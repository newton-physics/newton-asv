#!/usr/bin/env python3
"""Daily regression sweep over asv result files.

Sections:
  1. Machine freshness   -- active machines that stopped reporting
  2. Series continuity   -- disappeared/appeared benchmarks, version-hash mismatches
  3. Regression sweep    -- recent-window medians vs prior baseline per (machine, env)

Run from the newton-asv repo root. Flags are CANDIDATES: confirm each one against the
full series (series.py) and the workflow in SKILL.md before reporting.
"""

import argparse
import datetime
import glob
import json
import os
import statistics

SILENT_FLAG_DAYS = 3    # active machine with no data for longer -> flag
RETIRED_AFTER_DAYS = 60  # no data for longer -> considered retired, not flagged


def is_oscillating(history):
    """True if a chronological series alternates between levels rather than
    stepping once. A real step crosses the midline once (twice if it recovered);
    bimodal noise crosses it repeatedly."""
    if len(history) < 6:
        return False
    lo, hi = min(history), max(history)
    if lo <= 0 or hi / lo < 1.05:
        return False
    mid = (lo + hi) / 2
    sides = [v > mid for v in history]
    transitions = sum(a != b for a, b in zip(sides, sides[1:]))
    return transitions >= 3


def load_runs(root):
    """[(machine_dir, env, date_ms, parsed_json)] for all result files."""
    runs = []
    for mdir in sorted(os.listdir(root)):
        full = os.path.join(root, mdir)
        if not os.path.isdir(full) or mdir.startswith("."):
            continue
        for f in glob.glob(os.path.join(full, "*.json")):
            if f.endswith("machine.json"):
                continue
            try:
                d = json.load(open(f))
            except (json.JSONDecodeError, OSError):
                continue
            if "results" in d:
                runs.append((mdir, d.get("env_name", "?"), d.get("date", 0), d))
    return runs


def extract(d):
    """{(benchmark, param_string): value} for one result file."""
    cols = d.get("result_columns", [])
    out = {}
    for name, row in d["results"].items():
        if not isinstance(row, list) or not row:
            continue
        rec = dict(zip(cols, row))
        vals = rec.get("result")
        if vals is None:
            continue
        combos = [[]]
        for plist in rec.get("params") or []:
            combos = [c + [p] for c in combos for p in plist]
        if len(combos) != len(vals):
            combos = [[str(i)] for i in range(len(vals))]
        for c, v in zip(combos, vals):
            if isinstance(v, (int, float)):
                out[(name, ", ".join(c))] = v
    return out


def versions(d):
    """{benchmark: version_hash} for one result file."""
    cols = d.get("result_columns", [])
    if "version" not in cols:
        return {}
    vidx = cols.index("version")
    return {n: row[vidx] for n, row in d["results"].items()
            if isinstance(row, list) and len(row) > vidx}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default="results")
    ap.add_argument("--days", type=int, default=3,
                    help="recent window, relative to each machine's newest run (default 3)")
    ap.add_argument("--threshold", type=float, default=1.05,
                    help="flag ratio (default 1.05 = +/-5%%)")
    ap.add_argument("--baseline-n", type=int, default=8,
                    help="baseline runs before the window (default 8)")
    args = ap.parse_args()

    runs = load_runs(args.root)
    now = datetime.datetime.now()

    # --- 1. machine freshness ---
    print("=== 1. Machine freshness ===")
    latest_by_machine = {}
    for mdir, _, dt, _ in runs:
        latest_by_machine[mdir] = max(latest_by_machine.get(mdir, 0), dt)
    retired = []
    for mdir, dt in sorted(latest_by_machine.items()):
        age = (now - datetime.datetime.fromtimestamp(dt / 1000)).days
        stamp = datetime.datetime.fromtimestamp(dt / 1000).strftime("%Y-%m-%d")
        if age > RETIRED_AFTER_DAYS:
            retired.append(f"{mdir} (last {stamp})")
        elif age > SILENT_FLAG_DAYS:
            print(f"  FLAG: {mdir} silent for {age} days (last {stamp})")
        else:
            print(f"  ok:   {mdir} (last {stamp})")
    if retired:
        print(f"  retired (not flagged): {'; '.join(retired)}")

    # group runs per (machine, env), newest last
    bymachine = {}
    for mdir, env, dt, d in runs:
        bymachine.setdefault((mdir, env), []).append((dt, d))
    for lst in bymachine.values():
        lst.sort(key=lambda x: x[0])

    def split_window(lst):
        """(baseline_runs, recent_runs) using the machine's own newest run as anchor."""
        anchor = lst[-1][0]
        cutoff = anchor - args.days * 86400_000
        recent = [x for x in lst if x[0] > cutoff]
        base = [x for x in lst if x[0] <= cutoff][-args.baseline_n:]
        return base, recent

    active = {k: lst for k, lst in bymachine.items()
              if (now - datetime.datetime.fromtimestamp(lst[-1][0] / 1000)).days
              <= RETIRED_AFTER_DAYS}

    # --- 2. series continuity ---
    print("\n=== 2. Series continuity (disappeared/appeared benchmarks, hash mismatches) ===")
    bj_path = os.path.join(args.root, "benchmarks.json")
    current = {}
    if os.path.exists(bj_path):
        bj = json.load(open(bj_path))
        current = {k: v.get("version") for k, v in bj.items()
                   if isinstance(v, dict) and "version" in v}
    disappeared, appeared, mismatched = {}, {}, {}
    for (mdir, env), lst in sorted(active.items()):
        base, recent = split_window(lst)
        if not base or not recent:
            continue
        base_keys = set().union(*(set(d["results"]) for _, d in base))
        new_keys = set(recent[-1][1]["results"])
        for k in sorted(base_keys - new_keys):
            disappeared.setdefault(k, []).append(f"{mdir}/{env}")
        for k in sorted(new_keys - base_keys):
            appeared.setdefault(k, []).append(f"{mdir}/{env}")
        if current:
            for k, v in versions(recent[-1][1]).items():
                if k in current and v != current[k]:
                    mismatched.setdefault(k, []).append(f"{mdir}/{env}")
    for label, d in [("DISAPPEARED", disappeared), ("appeared", appeared),
                     ("HASH MISMATCH vs benchmarks.json", mismatched)]:
        for k, machines in sorted(d.items()):
            print(f"  {label}: {k} ({len(machines)} machine/envs)")
    if disappeared or mismatched:
        print("  -> rename or benchmark-source change: hash-rewrite DECISION needed"
              " (see rewrite-hashes skill)")
    if not (disappeared or appeared or mismatched):
        print("  none")

    # --- 3. regression sweep ---
    print("\n=== 3. Regression sweep (recent median vs baseline median) ===")
    report = []
    for (mdir, env), lst in sorted(active.items()):
        base, recent = split_window(lst)
        if len(base) < 3 or not recent:
            continue
        base_ex = [extract(d) for _, d in base]
        rec_ex = [extract(d) for _, d in recent]
        keys = set().union(*base_ex, *rec_ex)
        for k in sorted(keys):
            bvals = [e[k] for e in base_ex if k in e]
            rvals = [e[k] for e in rec_ex if k in e]
            if len(bvals) < 3 or not rvals:
                continue
            bmed, rmed = statistics.median(bvals), statistics.median(rvals)
            if bmed <= 0:
                continue
            ratio = rmed / bmed
            if ratio >= args.threshold or ratio <= 1 / args.threshold:
                spread = max(bvals) / min(bvals) if min(bvals) > 0 else float("inf")
                report.append((ratio, mdir, env, k, bmed, rmed,
                               len(bvals), len(rvals), spread,
                               is_oscillating(bvals + rvals)))
    report.sort(key=lambda r: -r[0])
    for ratio, mdir, env, (name, params), bmed, rmed, nb, nr, spread, osc in report:
        tags = ""
        if osc:
            tags += " OSCILLATING"
        if spread > 1.3:
            tags += " NOISY"
        p = f" [{params}]" if params else ""
        print(f"  {ratio:5.2f} {mdir[:26]:<26} {env:<20} {name}{p}"
              f"  {bmed:.4g}->{rmed:.4g} (n={nb}/{nr}, spread x{spread:.2f}){tags}")
    if not report:
        print("  none")


if __name__ == "__main__":
    main()
