---
name: rewrite-hashes
description: Use when a dashboard benchmark series ends or splits while the benchmark still runs — after newton renames a benchmark or changes its source (asv version hash), or when check-regressions flags hash mismatches or disappeared benchmarks.
---

# Rewrite Benchmark Hashes

## Overview

asv matches results to a dashboard series by benchmark key + `version` hash (hash of the benchmark source). When newton changes a benchmark, old result files keep the old hash and the dashboard starts a new series. `results/adenzler-asv-runner/replace_hash.sh` holds a name→current-hash map (must match `results/benchmarks.json`) and rewrites the hashes inside all result JSONs to reconnect history.

Prerequisite: at least one post-change automation run has landed, so `results/benchmarks.json` already contains the new hashes.

## Decision gate — before touching anything

Establish the facts per benchmark:

1. What changed? `git -C <newton> log -p <range> -- asv/` for the benchmark file AND the example it wraps (check imports in newton's `asv/benchmarks/`), where `<newton>` is a local checkout of github.com/newton-physics/newton.
2. Is there a step at the series boundary? (`series.py` from the check-regressions skill — note the magnitude per machine.)

Timing-irrelevant change (pure rename, comments, untimed setup) with no boundary step → **merge** (procedures below).

Anything else — workload, timed region, or scene changed, or a boundary step exists — is a product decision with no clean rule: continuous history is often worth more than strict comparability, so "the setup changed" does **not** imply "don't merge". Never decide this yourself. Present the evidence (what changed, step magnitude per machine) and ask the user, offering:

- **Merge**: history stays continuous; the change appears as a known, documented step in the series. Often right when it's still "the same benchmark", measured somewhat differently.
- **Don't merge**: old series ends, new baseline starts; drop/skip the replace_hash.sh entry with a comment documenting the exclusion (precedent: tiled-camera #3480, new scene).
- **Defer**: leave as-is until more post-change data exists to judge the step.

Raw old data stays in the result files either way; whichever way it goes, record the decision in the commit message and a script comment so it isn't re-litigated.

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
