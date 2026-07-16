#!/usr/bin/env python3
"""Dump the full time series of a benchmark per machine, with snapshot hashes.

Usage: series.py BENCHMARK_SUBSTRING [PARAM_FILTER]

PARAM_FILTER matches the repr'd param string, so quote accordingly: "'g1'" or "8192".
Use the printed snapshot hashes for (last-good, first-bad] bracketing across machines.
Run from the newton-asv repo root.
"""

import argparse
import datetime
import glob
import json
import os


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("benchmark", help="substring of the benchmark name")
    ap.add_argument("param_filter", nargs="?", help="substring of the param repr string")
    ap.add_argument("--root", default="results")
    ap.add_argument("--last", type=int, default=16, help="rows per machine (default 16)")
    ap.add_argument("--all", action="store_true", help="show the entire series")
    args = ap.parse_args()

    for mdir in sorted(os.listdir(args.root)):
        full = os.path.join(args.root, mdir)
        if not os.path.isdir(full) or mdir.startswith("."):
            continue
        rows = []
        for f in glob.glob(os.path.join(full, "*.json")):
            if f.endswith("machine.json"):
                continue
            try:
                d = json.load(open(f))
            except (json.JSONDecodeError, OSError):
                continue
            if "results" not in d:
                continue
            cols = d.get("result_columns", [])
            for name, row in d["results"].items():
                if args.benchmark not in name or not isinstance(row, list):
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
                    pstr = ", ".join(c)
                    if args.param_filter and args.param_filter not in pstr:
                        continue
                    if isinstance(v, (int, float)):
                        rows.append((d.get("date", 0), d.get("commit_hash", "?")[:9],
                                     d.get("env_name", "?"), pstr, v))
        if not rows:
            continue
        rows.sort()
        print(f"\n=== {mdir} ===")
        for dt, ch, env, pstr, v in rows if args.all else rows[-args.last:]:
            ds = datetime.datetime.fromtimestamp(dt / 1000).strftime("%m-%d")
            p = f" [{pstr}]" if pstr else ""
            print(f"  {ds} {ch} {env:<20}{p} {v:.5g}")


if __name__ == "__main__":
    main()
