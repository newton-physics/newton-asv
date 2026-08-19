# Newton ASV Regression Report — 2026-08-19

**Window:** since last daily check (2026-08-17). **Data through 2026-08-19** (SC-PV desktops);
**Spark + both Jetsons through 2026-08-18** (all "ok" — Jetsons recovered from the 08-17 staleness).
**Setup:** `git pull`-ed `newton-asv` first (MANDATORY — rebased the local 08-17 report commit onto
`origin/main` HEAD `980bacbd` to pick up 11 new data commits; ahead 1, **NOT pushed**).
Snapshot→commit mapping: `~/repos/newton` fetched to `origin/main` HEAD `f244e7ed` (#3949). newton uses
squash-merges, so first-parent main is linear and snapshot ordering is unambiguous.

Newest snapshots this window: desktops **08-19 `8f1dbad79`** (#3960 Kamino UT discovery) and 08-18
`6d3fdf6f7` (#3930); jetson_agx_orin 08-18 `92abd04b7` (#3893); jetson_agx_thor 08-18 `6d3fdf6f7`;
Spark 08-18 `7befae04c` (#3744).

## Data freshness
- Active fleet all "ok": SC-PV-02 / SC-PV-10 last **2026-08-19** (`8f1dbad79`); SC-PV-SPARK-PS-01 last
  **2026-08-18** (`7befae04c`); jetson_agx_orin / jetson_agx_thor last **2026-08-18**.
- **RESOLVED vs 08-17:** the Jetson 3-day-stale soft flag has cleared — both Jetsons ran 08-18 (1 day
  old). No machine is >3 days silent among the active fleet.
- FLAG SC-PV-SPARK-PS-07 (GB10): silent 56 days (last 2026-06-23) — long dormant.
- FLAG adenzler-horde-L40S: silent 27 days (last 2026-07-22) — still the only py3.13 runner besides the
  SC-PV desktops; its continued absence still blocks any py3.13-only cross-confirmation.
- Retired (not flagged): adenzler-asv-runner, ershi-asv, ershi-asv-runner.

## Series continuity
- DISAPPEARED (1 machine/env, unchanged): `bench_sensor_tiled_camera.FastSensorTiledCamera.time_rendering_pixel_priority_{color_depth,color_only,depth_only}`.
  Only ever existed on the now-silent adenzler-horde-L40S; a rename/removal from a sensor-benchmark
  refactor. No exclusion in `replace_hash.sh`. Decision unchanged: LOW urgency — let it age out. Not a regression.
- APPEARED (benchmark-suite expansion, benign — NOT renames of existing perf series): the `track_*`
  metric-track / `KpiDRLegs` / `FastMetricsDRLegs` / `FastMetrics*` / `Notify*` / mujoco `track_*` families
  continuing to fill baselines on machine/envs that only recently started reporting them (each "1
  machine/env"). New metrics establishing their own baselines, not renames — the fully-qualified names of
  the existing perf series (e.g. `NotifyDRLegs.time_notify_*`) are unchanged and continuous. Same conclusion
  as 08-14/08-17; no rewrite forced.
- Kamino harness churn this window (#3959 "Remove Kamino internal benchmark", #3960 "Update Kamino UT script
  to discover both internal and newton tests") produced **no public-asv DISAPPEARED** — the removed item was
  a Kamino-internal benchmark not in the published set. Watch next sweep in case a public series drops.
- No version-hash mismatches.

## Findings

### 1. bench_kamino.NotifyDRLegs.time_notify_* — REGRESSION ~2×–7× — dependency bump (Warp 1.16 pin, #3780) — P1 — **PERSISTING, NOT recovered**
**Answer to the recovery question: NO — still elevated, no recovery through the newest snapshots
(desktops 08-19 `8f1dbad79`, Jetsons 08-18).** The clean worst-hit sub-metric
`time_notify_model_properties` shows **no down-step at 08-18 or 08-19** — flat on the Warp-elevated plateau:
- jetson_agx_thor: pre-step 08-03 `10402ecba` **8.76e-6** → **08-18 `6d3fdf6f7` 6.23e-5 (~7.1×)**.
- jetson_agx_orin: pre-step 08-01 ~1.65–1.74e-5 → **08-18 `92abd04b7` 1.14e-4 (~6.7×)**.
- SC-PV-02: flat plateau ~4.2–4.7e-5; 08-18 4.65e-5 (py3.12) / 4.56e-5 (py3.13); 08-19 4.24e-5 (py3.13).
- SC-PV-10: flat plateau ~3.6–4.0e-5; 08-18 4.04e-5 (py3.12) / 3.64e-5 (py3.13); 08-19 3.84e-5 (py3.13).
- SC-PV-SPARK-PS-01: ~3.7e-5; 08-18 3.72e-5.
Rest of the family (shape/body/joint/dof/actuator/all/model) likewise flat on the elevated plateau. No
candidate fix (the #3859 sampling fix or #3849 Warp-nightly bump, both from earlier windows) has moved it.
- **Bracket / classification: unchanged** — `(10402ecba, 274766302]`, contains **#3780 "Stabilize Warp 1.16
  dependency"** (Jan Carius, jcarius-nv), moving the ASV install pin `warp-lang==1.16.0.dev20260716` →
  `warp-lang==1.16.0`. DEPENDENCY BUMP; no `asv/` change in the bracket.
- **Status: PERSISTING** (16+ consecutive snapshots, all machines, both py). The SC-PV-10 **py3.13**
  sub-metric down-swings the sweep flagged this window (`notify_all` 0.80×, `body` 0.71×, `shape` 0.75×,
  `actuator` 0.77×, `joint` 0.79×, `joint_dof` 0.79× — all NOISY, spread ×1.6–2.25, single machine/env) are
  the SAME py3.13 bimodality noted 08-14/08-17, NOT a fix: `model_properties` on that exact runner is flat
  ~3.6–3.9e-5, and the same sub-metrics do not move on the Jetsons or on SC-PV-10 py3.12. Dismissed as
  within-plateau py3.13 noise.
- **Action:** gchat/Slack drafts prepared (in handoff) — HELD for Dylan. Do NOT file/post.

### 2. bench_kamino.NotifyDRLegs.time_notify_body_inertial_properties — SECOND REGRESSION ~1.3×–1.9× — product change (#3858 Kamino body-inertial validation kernel) — P2 — PERSISTING (no growth)
Step at 08-11 `98ba6dc65`, **holds through 08-18/08-19** at the same magnitude (no recovery, no growth):
- SC-PV-02 py3.13 ~0.60e-3 (08-17/08-18) — py3.12 ~0.36–0.37e-3. SC-PV-10 py3.12 ~0.31–0.32e-3, py3.13
  ~0.37–0.39e-3. Spark ~0.41e-3. jetson_thor ~0.64e-3 (~1.25×). jetson_orin ~1.2e-3 (~1.20×).
- 08-19 py3.13 single-point jitter (SC-PV-02 dropped to 0.41e-3, SC-PV-10 rose to 0.55e-3) is the py3.13
  bimodality, not a change — both sit inside the established plateau band.
- Bracket/classification unchanged: `(87189a218, 98ba6dc65]` → **#3858 "[Kamino] check massless runtime
  update"** (Ruben Grandia) adds a `validate_body_inertial_updates_kernel` launch on every body-inertial
  notify — why only `body_inertial_properties` stepped while `model_properties` stayed on its Warp-elevated
  plateau. PRODUCT CHANGE, no `asv/` change. Likely intentional correctness cost.
- **Status: PERSISTING.** Lower priority than Finding 1.

### 3. setup.bench_sdf.FastBuildSdf.time_build_sdf [128] — py3.13-DESKTOP REGRESSION ~1.3× — product change (#3904 SDF-texture rewrite) — **STATUS UPGRADE since 08-17: WATCH → CONFIRMED sticky**
The 08-17 report flagged this as a 2-snapshot "watch for a third point." It is now a **clean sustained step
across four consecutive snapshots** (08-14 → 08-17 → 08-18 → 08-19) on **both py3.13 desktops**:
- SC-PV-02 py3.13: pre ~0.138 → **0.186 / 0.186 / 0.187 / 0.179 (~1.35×)**.
- SC-PV-10 py3.13: pre ~0.131–0.139 → **0.179 / 0.179 / 0.178 / 0.186 (~1.31×)**.
- py3.12 desktops: SC-PV-02 ~flat 0.13–0.137; SC-PV-10 crept ~0.13 → ~0.159 (~1.2×, less clean / noisier).
- **Env-dependent, net still FAVORABLE across the fleet** (unchanged): the big wins hold — Spark ~0.583 →
  ~0.21 (**~0.36×**), jetson_thor ~0.77 → ~0.65 (**~0.85×**); jetson_orin ~0.84 → ~0.88 (~1.05×, mild up).
- **Classification: PRODUCT CHANGE (SDF data-structure / texture-storage change), env-dependent.** Same
  08-14 boundary and same **#3904 "Accelerate SDF and hydroelastic collision"** (nvtw) that heavily rewrites
  `sdf_texture.py`. The py3.13-desktop ~1.3× is now confirmed real and sticky (4 snapshots), not noise — a
  memory-layout/representation change different GPUs+runtimes respond to differently. **This is the one
  status change since 08-17.** Worth a heads-up to nvtw as a confirmed py3.13 SDF-build cost of #3904; net
  fleet impact remains positive, so not P1/P2.

### 4. bench_contacts.FastExampleContactHydroWorkingDefaults.time_simulate — IMPROVEMENT ~0.67×–0.84× — product change (#3904) — HOLDING (not new; from 08-14)
The clean fleet-wide hydroelastic speedup from #3904 (bracket `(8ce54fac8, 10141065c]`) is **stable at the
improved level**: jetson_thor ~0.67×, Spark ~0.77–0.83×, SC-PV desktops ~0.82–0.84×. Still flagged by the
sweep only because the baseline-8 window still reaches back before the 08-14 step. Specific to the
hydroelastic path (`ContactSdfDefaults` unchanged). Favorable — no action.

### No new culprit/PR regression this window
Commits landed 08-17→08-19 (first-parent): #3960, #3818, #3857, #3893, #3930, #3924, #3919, #3959, #3744,
#3918, #3869, #3898, #3838, #3911, #3924, #3911. None produced a clean cross-machine step in a non-noise
benchmark. **WATCH next sweep: #3918 "Improve convex collision kernel performance"** (landed ~08-18) — only
one post-snapshot so far (too early per the second-snapshot rule); no clear contact/collision step yet.

## Dismissed flags
- `teleop_mujoco.TeleopMuJoCo.track_object_displacement_m` (ratios 0.02×–2.06×, spreads up to ×101),
  `track_loop_time_cv_pct`, `track_hand_object_contact_frame_pct`, `track_*_loop_ms`, `track_real_time_factor`,
  `track_sustainable_physics_step_hz` — dominate BOTH ends of the sweep. Physical-quality / CV / loop-timing
  metrics on the teleop scene, inherently oscillating and env-specific (mujoco/mjwarp cpu_eager/cpu_graph/
  cuda_graph). Pure noise, not perf.
- `*.track_steady_state_gpu_memory` (jetson + spark, FastHumanoid/FastG1/FastMetrics*/Anymal/Quadruped/
  Kamino, ×1.3–7 spread NOISY) — memory-sampling noise, both directions.
- `bench_mujoco.RealtimeHumanoidPhysics.track_step_time_cv_pct` (0.33×–2.22×, spread up to ×16) — CV metric.
- `bench_mujoco Fast*.track_solver_niter_max` 5↔6/7 — integer solver-iteration oscillation.
- `setup.bench_model.{Fast,Kpi}Initialize*` time/peakmem (~0.73–1.38×, OSCILLATING) — single-shot compile/
  init benchmarks jitter ±15%+.
- `compilation.bench_example_load.SlowExample*` (~0.89–1.16× OSCILLATING) — load-time jitter.
- `bench_kamino.FastMetricsDRLegs`/`KpiDRLegs` `track_*` (real_time_factor / p95_step_time / mean_world_step
  ~0.92–1.09×) — newly-APPEARED metrics still filling baselines; baseline-fill noise, not a perf step.
- `bench_kamino.FastDRLegs.time_simulate` (~0.90–0.92× on SC-PV-02/10/Spark) — recent values are FLAT since
  ~08-13 (SC-PV-10 ~1.07, Spark ~1.19); the sub-1 ratio is a baseline-window artifact (the baseline reaches
  back to the early-August higher plateau). No step in the reporting window.
- `bench_heightfield` / `bench_inverse_dynamics` / `bench_implicit_mpm` single-machine SC-PV-10 py3.13
  down-swings (0.84–0.90× NOISY) — single machine/env, py3.13 bimodality, not cross-confirmed.
- NotifyDRLegs SC-PV-10 py3.13 sub-metric down-swings — see Finding 1 (within-plateau py3.13 noise).

## Report-back one-liner
Top item: **NotifyDRLegs / Warp-1.16 ~7× — STILL NOT recovered** (flat on the elevated plateau through
desktops 08-19 / Jetsons 08-18; the py3.13 down-swings are bimodality, not a fix). **No brand-new
culprit/PR regression** since 08-17. One status change: the #3904 py3.13-desktop `FastBuildSdf[128]` ~1.3×
is now **confirmed sticky** (4 snapshots, upgraded from "watch") — env-dependent, net fleet still favorable.
Body-inertial #3858 ~1.3–1.9× and the #3904 hydroelastic ~0.67–0.84× improvement both persist unchanged.
