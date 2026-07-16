---
name: rewrite-hashes
description: Use when a dashboard benchmark series ends or splits while the benchmark still runs — after newton renames a benchmark or changes its source (asv version hash), or when check-regressions flags hash mismatches or disappeared benchmarks.
---

# Rewrite Benchmark Hashes

## Overview

asv matches results to a dashboard series by benchmark key + `version` hash (hash of the benchmark source). When newton changes a benchmark, old result files keep the old hash and the dashboard starts a new series. `results/adenzler-asv-runner/replace_hash.sh` holds a name→current-hash map (must match `results/benchmarks.json`) and rewrites the hashes inside all result JSONs to reconnect history.

Prerequisite: at least one post-change automation run has landed, so `results/benchmarks.json` already contains the new hashes.

## Decision gate — before touching anything

Merging history claims "same workload, numbers comparable". Verify per benchmark:

1. What changed? `git -C ~/git/newton log -p <range> -- asv/` for the benchmark file AND the example it wraps (check imports in newton's `asv/benchmarks/`).
2. Is there a step at the series boundary? (`series.py` from the check-regressions skill)

- Timing-irrelevant change (rename, comments, untimed setup) and no boundary step → **merge** (procedures below).
- Workload / timed region / scene changed, or a boundary step exists → **do NOT merge**: remove or don't add the entry in replace_hash.sh, with a comment documenting the exclusion. Precedent: tiled-camera #3480 (new scene — old series deliberately ends 2026-07-14).
- Unsure → ask the user. A wrong merge bakes a fake step into the dashboard permanently; the old series stays recoverable either way, but nobody notices a quiet bad merge.

Never add a benchmark to replace_hash.sh just because an audit finds it "missing" — absence may be a deliberate exclusion, and the reflex once silently rewrote 109 result files across a timed-region change.

## Procedures

| Case | What to do | Precedent commit |
|---|---|---|
| Same name, new hash | Update the entry in replace_hash.sh from benchmarks.json; run `./replace_hash.sh <path-to-results>` | most history of the script |
| Renamed, hash unchanged | Rename the key in all historical result JSONs; update script entries | `1cd00414` |
| Renamed, old+new keys coexist in files | Merge rows: union the param combos so retired values stay under their old params | `292e16b9` |

`git show <precedent>` shows the exact mechanics for the rename/merge cases.

## Verify and land

- `git diff --stat`: only intended files. Spot-check a hunk: only 64-hex version strings (or renamed keys) changed.
- Re-dump one affected series: continuous, no artificial boundary step.
- Convention: these maintenance commits land directly on main (data repo). Remote pushes still need explicit user approval.

## Common mistakes

- Running before benchmarks.json has the new hashes — rewrites history to stale values.
- Forgetting the script defaults to its *own* directory — pass the results root explicitly.
- Treating replace_hash.sh as an exhaustive registry. It is a merge tool; a benchmark not listed is a decision, not an oversight.
