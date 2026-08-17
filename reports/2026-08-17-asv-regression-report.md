# Newton ASV Regression Report — 2026-08-17

**Window:** since last daily check (2026-08-14). **Data through 2026-08-17** (SC-PV desktops + Spark);
**Jetsons through 2026-08-14** (3 days stale — see freshness).
**Setup:** `git pull`-ed `newton-asv` first (MANDATORY). Pulled to HEAD `d6e6d266` (08-17 data).
Snapshot→commit mapping: `~/repos/newton` fetched to `origin/main` HEAD `8119b6e6` (#3947). newton uses
squash-merges, so first-parent main is linear and snapshot ordering is unambiguous.

## Data freshness
- Active fleet reporting: SC-PV-02, SC-PV-10, SC-PV-SPARK-PS-01 last **2026-08-17** (`8119b6e6b`).
- FLAG (soft) both Jetsons `jetson_agx_orin` / `jetson_agx_thor`: last run **2026-08-14** (`7bb6d02d8`),
  i.e. 3 days stale as of 08-17. The sweep marks them "ok" (exactly at the 3-day threshold), but the
  Jetson P1 non-recovery evidence below is therefore "through 08-14", not 08-17. Watch for a >3-day gap
  tomorrow.
- FLAG SC-PV-SPARK-PS-07 (GB10): silent 54 days (last 2026-06-23) — long dormant.
- FLAG adenzler-horde-L40S: silent 26 days (last 2026-07-22) — still the only py3.13 runner besides the
  SC-PV desktops; its continued absence still blocks any py3.13-only cross-confirmation.
- Retired (not flagged): adenzler-asv-runner, ershi-asv, ershi-asv-runner.

## Series continuity
- DISAPPEARED (1 machine/env, unchanged): `bench_sensor_tiled_camera.FastSensorTiledCamera.time_rendering_pixel_priority_{color_depth,color_only,depth_only}`.
  Only ever existed on the now-silent adenzler-horde-L40S; a rename/removal from a sensor-benchmark
  refactor. No exclusion in `replace_hash.sh`. Decision unchanged: LOW urgency — let it age out. Not a regression.
- APPEARED (benchmark-suite expansion, benign — NOT renames of existing perf series): the big "appeared"
  list is the `track_*` metric-track / `KpiDRLegs` / `FastMetrics*` / `Notify*` families continuing to fill
  baselines on machine/envs that only recently started reporting them (each shows "1 machine/env"). These
  are genuinely new metrics establishing their own baselines, not renames — the fully-qualified names of the
  existing perf series (e.g. `NotifyDRLegs.time_notify_*`) are unchanged and continuous. The sweep's blanket
  "hash-rewrite DECISION needed" line is triggered by the appeared-count; no rewrite is actually forced (same
  conclusion as 08-14). 
- No version-hash mismatches.

## Findings

### 1. bench_kamino.NotifyDRLegs.time_notify_* — REGRESSION ~2x–7x — dependency bump (Warp 1.16 pin, #3780) — P1 — **PERSISTING, NOT recovered**
**Answer to the recovery question: NO.** The ~7x Warp-1.16-pin regression has **not** recovered. Neither
candidate fix moved the clean signal:
- #3859 "Fix NotifyDRLegs ASV sampling" (Ruben Grandia, ~08-10) and the #3849 Warp-nightly bump (in the
  08-10 bracket) both landed *within* the flat elevated plateau — `time_notify_model_properties` (the
  cleanest, worst-hit sub-metric) shows **no down-step at 08-10, 08-11, 08-13, 08-14 or 08-17**.
- **Magnitude (worst hit `time_notify_model_properties`), still elevated at newest snapshot:**
  - jetson_agx_thor: pre-step 08-03 `10402ecba` 8.76e-6 → plateau; **08-14 `7bb6d02d8` 5.90–6.36e-5 (~7x)**.
  - jetson_agx_orin: pre-step 08-01 `ee84505ae` 1.65–1.74e-5 → **08-14 `7bb6d02d8` 1.14–1.16e-4 (~6.7x)**.
  - SC-PV-02: flat plateau ~4.2–4.76e-5; **08-17 `8119b6e6b` 4.67e-5 (py3.12) / 4.76e-5 (py3.13)**.
  - SC-PV-10: flat plateau ~3.5–3.9e-5; **08-17 3.80e-5 / 3.86e-5**.
  - SC-PV-SPARK-PS-01: ~3.4–4.1e-5; 08-17 3.37e-5.
  Rest of the family (shape/body/joint/dof/actuator/all) likewise flat on the Warp-elevated plateau; the
  cross-machine `shape_properties` series is flat ~4.2e-4 (thor) / ~7.8e-4 (orin) through 08-14 with no step.
- **Bracket / classification: unchanged from 08-14** — `(10402ecba, 274766302]`, contains **#3780
  "Stabilize Warp 1.16 dependency"** (Jan Carius, jcarius-nv), moving the ASV install pin
  `warp-lang==1.16.0.dev20260716` → `warp-lang==1.16.0`. DEPENDENCY BUMP; no `asv/` change in the bracket.
- **Status: PERSISTING** (14 consecutive snapshots, all machines, both py). The SC-PV-10 py3.13 down-swings
  the sweep flagged this window (notify_all 0.66x, shape/body/joint 0.57–0.58x, NOISY, spread x1.6–2.3) are
  the SAME py3.13 bimodality noted 08-14, NOT a fix: on that exact machine/env `model_properties` is flat
  ~3.8e-5, and the same sub-metrics on the Jetsons and on SC-PV-10 py3.12 do not move. Dismissed as
  within-plateau noise.
- **Action:** Slack draft prepared (below) — HELD for Dylan. Do NOT file/post.

### 2. bench_kamino.NotifyDRLegs.time_notify_body_inertial_properties — SECOND REGRESSION ~1.2x–1.9x — product change (#3858 Kamino body-inertial validation kernel) — P2 — PERSISTING
- Step at 08-11 `98ba6dc65`, **holds through 08-17** at the same magnitude (no recovery, no growth):
  - jetson_agx_thor: plateau ~5.13e-4 → 6.29e-4 (08-11) → **08-14 6.39–6.47e-4 (~1.25x)**.
  - jetson_agx_orin: ~1.02e-3 → **08-14 1.21–1.26e-3 (~1.20x)**.
  - SC-PV-02 py3.12 ~1.9e-4 → **08-17 3.73e-4 (~1.9x)**; py3.13 ~3.5e-4 → **08-17 6.14e-4 (~1.7x)**.
  - SC-PV-10 py3.12 ~1.77e-4 → **08-17 3.09e-4 (~1.7x)**; py3.13 ~3.7–3.8e-4 (noisy/flat).
  - SC-PV-SPARK-PS-01 ~2.7e-4 → **08-17 4.17e-4 (~1.5x)**.
- Bracket/classification unchanged from 08-14: `(87189a218, 98ba6dc65]` → **#3858 "[Kamino] check massless
  runtime update"** (Ruben Grandia) adds a `validate_body_inertial_updates_kernel` launch on every
  body-inertial notify — precisely why only `body_inertial_properties` stepped while `model_properties`
  stayed on its (Warp-elevated) plateau. PRODUCT CHANGE, no `asv/` change. Likely intentional correctness cost.
- **Status: PERSISTING.** Lower priority than Finding 1; heads-up to Kamino owner already noted 08-14.

### 3. bench_contacts.FastExampleContactHydroWorkingDefaults.time_simulate — IMPROVEMENT ~0.67x–0.92x — product change (#3904) — **NEW since 08-14**
- **Machines/envs:** ALL — SC-PV-02, SC-PV-10 (both py), SC-PV-SPARK-PS-01, jetson_agx_orin, jetson_agx_thor.
- **Magnitude (clean step DOWN at the 08-14 snapshot, holds through 08-17):**
  - jetson_agx_thor: ~0.251 (08-13 `8ce54fac8`) → **0.168 (08-14 `7bb6d02d8`) (~0.67x)**.
  - SC-PV-SPARK-PS-01: ~0.106 → **0.083 (~0.78x)**, held 08-17.
  - SC-PV-02 py3.12 ~0.060 → **0.050 (~0.82x)**; py3.13 ~0.061 → **0.052 (~0.85x)**.
  - SC-PV-10 py3.12 ~0.059 → **0.050 (~0.83x)**; py3.13 ~0.062 → **0.052 (~0.85x)**.
  - jetson_agx_orin: ~0.36–0.39 → **~0.35 (~0.92x)** (smaller/noisier, but same direction).
- **Bracket (intersected across machines):** latest last-good = jetson 08-13 `8ce54fac8`; earliest
  first-low = Spark 08-14 `10141065c` → **`(8ce54fac8, 10141065c]`**, 6 commits:
  - **`eaed8a07` Accelerate SDF and hydroelastic collision (#3904)  ← SUSPECT** (nvtw)
  - `10141065` (#3730 USD cable), `0c4870fb` (#3821 assets), `f56650f4` (#3912 usd-schemas),
    `6ba9c369` (#3887 docs), `e296e1c8` (#3685 MJCF site actuators).
- **Classification: PRODUCT CHANGE (improvement).** No `asv/` change in the bracket. #3904 rewrites the
  hydroelastic collision path (`sdf_hydroelastic.py` +564, `contact_reduction_hydroelastic.py`,
  `sdf_contact.py`, `sdf_texture.py`) — an on-the-nose match for a `ContactHydro*` speedup, and it is
  *specific to hydroelastic*: `ContactSdfDefaults` did NOT get a fresh 08-14 step (jetson_thor flat 0.244→0.242,
  Spark slightly up), confirming the acceleration targets the hydroelastic branch. Favorable — no action.

### 4. setup.bench_sdf.FastBuildSdf.time_build_sdf [128] — MIXED env-dependent side-effect of #3904 — NEW, minor, WATCH
- Same 08-14 snapshot boundary and same #3904 (which heavily rewrites `sdf_texture.py` +577, the SDF build/
  storage path). Response is **hardware/env-dependent**, opposite directions across the fleet:
  - **IMPROVED:** SC-PV-SPARK-PS-01 ~0.59 → **0.22 (~0.37x)** (held 08-17); jetson_agx_thor ~0.77 → **0.63–0.65 (~0.83x)**.
  - **REGRESSED (modest):** SC-PV-02 py3.13 ~0.138 → **0.186–0.187 (~1.35x)** (2 snapshots, 08-14 + 08-17);
    SC-PV-10 py3.13 ~0.139 → **0.178–0.179 (~1.29x)** (2 snapshots); jetson_agx_orin ~0.84 → ~0.88 (~1.05x).
  - **FLAT:** SC-PV-02 py3.12 (~0.12), SC-PV-10 py3.12 (~0.13–0.16, noisy).
- **Classification: PRODUCT CHANGE (SDF data-structure change), env-dependent.** The py3.13-desktop ~1.3x
  is a real 2-snapshot step but is *env-specific* (py3.12 flat on the same physical machines, and Spark/thor
  went strongly the other way), so it is not a straightforward product regression in the build path — it is a
  memory-layout / representation change that different GPUs+runtimes respond to differently. Net across the
  fleet is favorable (the big wins on Spark/thor dominate). Not a P1/P2. WATCH the py3.13 desktops for a
  third snapshot to confirm the step is sticky; if it holds, flag to nvtw as a py3.13 SDF-build cost of #3904.

## Dismissed flags
- `teleop_mujoco.TeleopMuJoCo.track_object_displacement_m` / `track_hand_object_contact_frame_pct` /
  `track_loop_time_cv_pct` / `track_*_loop_ms` / `track_real_time_factor` / `track_sustainable_physics_step_hz`
  — dominate the top AND bottom of the sweep (ratios 0.02–6.0, spreads up to x52). Physical-quality /
  coefficient-of-variation / loop-timing metrics on the teleop scene, inherently oscillating and env-specific
  (mujoco/mjwarp cpu_eager/cpu_graph/cuda_graph). Pure noise, not perf.
- `*.track_steady_state_gpu_memory` (jetson + spark, FastHumanoid/FastG1/FastAllegro/FastKitchenG1/Anymal/
  Quadruped/Kamino, x1.4–8 spread NOISY) — memory-sampling noise, both directions.
- `bench_mujoco.RealtimeHumanoidPhysics.track_step_time_cv_pct` (0.19–1.68x, spread up to x18) — CV metric,
  inherently noisy.
- `bench_mujoco Fast*.track_solver_niter_max` 5↔6 — integer solver-iteration oscillation.
- `setup.bench_model.{Fast,Kpi}Initialize*` time/peakmem (~0.75–1.41x, OSCILLATING) — single-shot compile/
  init benchmarks jitter ±15%+.
- `compilation.bench_example_load.SlowExample*` (~0.89–1.10x OSCILLATING) — load-time jitter.
- `bench_cpu.CpuMuJoCoAnt` / `CpuIKFranka` / `bench_viewer.FastViewerGL.time_rendering_frame` — single
  machine/env, OSCILLATING, not cross-confirmed.
- `bench_heightfield` / `bench_inverse_dynamics` / `bench_implicit_mpm` single-machine SC-PV-10 py3.13
  down-swings (0.58–0.73x NOISY) — single machine/env, py3.13 bimodality, not cross-confirmed.
- NotifyDRLegs SC-PV-10 py3.13 sub-metric down-swings — see Finding 1 (within-plateau py3.13 noise).

## Drafted Slack message — HELD for Dylan (do NOT post)

Channel: #newton-dev (ASV items).

> :warning: *ASV daily (2026-08-17) — NotifyDRLegs / Warp-1.16 slowdown still NOT recovered; plus a hydroelastic speedup*
>
> Following up on the `bench_kamino.NotifyDRLegs.time_notify_*` ~2–7× regression from the Warp 1.16 pin (#3780): **still present, no recovery.** The two candidate fixes did not move the clean signal — #3859 "Fix NotifyDRLegs ASV sampling" and the #3849 Warp-nightly bump both land inside the flat elevated plateau, and `time_notify_model_properties` shows no down-step at any snapshot 08-10 → 08-17. Worst hit (~7×) `time_notify_model_properties`:
> • jetson_agx_thor: 8.8e-6 → ~6.0e-5 s (through 08-14)
> • jetson_agx_orin: 1.7e-5 → ~1.15e-4 s (through 08-14)
> • SC-PV desktops: flat elevated plateau through 08-17
> Still every machine, py3.12 + py3.13. The SC-PV-10 py3.13 sub-metric down-swings this week are py3.13 bimodality, not a fix (model_properties on that same runner is flat). *Ask stands:* is the extra per-launch notify overhead in stable Warp 1.16.0 expected, or a Warp-side regression to escalate? Re-pinning the last-good Warp build is the quick mitigation.
>
> :white_check_mark: *Good news, separate:* **#3904 "Accelerate SDF and hydroelastic collision"** (landed 08-14) gives a clean fleet-wide speedup on `bench_contacts.FastExampleContactHydroWorkingDefaults.time_simulate`: jetson_thor ~0.67×, Spark ~0.78×, SC-PV desktops ~0.82–0.85×. Specific to the hydroelastic path (ContactSdf unchanged). One caveat to watch: the same PR's SDF-texture rewrite shifts `FastBuildSdf[128]` build time env-dependently — big win on Spark (~0.37×)/thor, but a modest ~1.3× on the py3.13 desktops (2 snapshots so far). Watching for a third point before flagging.
>
> Dashboard: https://newton-physics.github.io/newton-asv/ · PRs: #3780, #3904
>
> _(Also still open: the smaller ~1.2–1.9× second step in `time_notify_body_inertial_properties` from #3858's body-inertial validation kernel — unchanged since 08-11. Likely intentional correctness cost.)_
