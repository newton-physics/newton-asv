---
name: check-regressions
description: Use when checking newton benchmark dashboard data (asv results) for performance regressions, when asked whether anything regressed in the last days, or when investigating a step change or anomaly in a benchmark series in this repo.
---

# Check Regressions

## Overview

Daily regression triage over the asv result JSONs in `results/<machine>/`. Core principle: the sweep only produces *candidates* — a finding is real only after the full series confirms it and the culprit bracket has been intersected **across machines**.

Requires a local newton checkout to map snapshots to commits — `<newton>` below; locate or clone one (github.com/newton-physics/newton) before starting.

## Workflow

Run scripts from the repo root.

1. **Sweep + health**: `python3 .claude/skills/check-regressions/scripts/check_regressions.py` (see `--help`). Reports machine freshness, series-continuity issues (disappeared benchmarks, version-hash mismatches), and median-vs-baseline flags.
2. **Triage each flag**: `python3 .claude/skills/check-regressions/scripts/series.py <benchmark-substring> [param-filter]` — full per-machine series with snapshot hashes. Judge noise from the data, not from a fixed list: an OSCILLATING tag means the series alternates between levels instead of stepping once — dismiss when the full series confirms recent values sit inside the historical envelope (oscillation can be env-specific: the same benchmark may be bimodal on py3.12 and flat on py3.13, and single-shot compile-time benchmarks jitter ±15%). A real step transitions once — or twice if it recovered, which is still a finding: report it as resolved-by.
3. **Bracket the culprit**: snapshots are sparse — the culprit is in `(last-good, first-bad]`. Machines benchmark *different* snapshots: intersect the brackets from every machine/env before enumerating (Jetsons often ran an intermediate snapshot that pins a single commit). Then `git -C <newton> log --oneline --first-parent LASTGOOD..FIRSTBAD`.
4. **Classify every confirmed step — improvements too**:
   - **workload change**: `git -C <newton> log A..B -- asv/` is non-empty, or the example the benchmark wraps changed (check the benchmark's imports in newton's `asv/benchmarks/`). A step from these is a redefinition, not a perf change; it may need a hash-rewrite decision.
   - **dependency bump**: diff the `requirements` dict between the last-good and first-bad result JSONs.
   - **product change**: otherwise — name suspect commits from the bracket.
   - To pick between suspects (including for recoveries), read their full messages and PR bodies: `git -C <newton> log -1 --format=%B <sha>`, then `gh pr view <N> --repo newton-physics/newton` — fix PRs often name the exact example or benchmark.
5. **Report** with the template below.

## Report template

The three flag sections are REQUIRED even when empty ("none"):

- **Data freshness**: active machines silent >3 days.
- **Series continuity**: disappeared/renamed benchmarks or hash mismatches. For each: "hash-rewrite decision needed" → use the `rewrite-hashes` skill. If the decision was already made (documented as an exclusion comment in `replace_hash.sh`), say so instead. DISAPPEARED flags age out once the baseline window passes the change.
- **Findings**: per finding — benchmark, machines + magnitude, bracket (snapshot hashes), classification, suspect commit/PR, status (persisting | resolved-by X).
- **Dismissed flags**: one line each — what the sweep flagged and why you dismissed it.

## Common mistakes

- Bracketing from a single machine's snapshot sequence → a 30-commit suspect list where cross-machine intersection pins 1.
- Dismissing or confirming a flag from its tags alone — OSCILLATING/NOISY are hints computed on a short window; the full series decides.
- Reporting a large improvement without classifying it — a 10× step is usually a harness/workload change (e.g. graph capture added to examples), not free perf.
- Treating a benchmark rename or new scene as a regression/improvement.
- Trusting a single post-step data point — wait for a second snapshot before closing.
- Dismissing a sustained step on one machine class as noise because other machines moved differently — hardware responds differently to the same change; a step that holds for ≥2 snapshots gets bracketed and classified, whatever the other machines did.
- Param filters in series.py match repr strings — `'g1'` includes the quotes.
