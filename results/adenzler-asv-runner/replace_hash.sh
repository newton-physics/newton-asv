#!/bin/bash

# Usage: ./replace_hash.sh [DIRECTORY]
# If no directory is given, operates on the script's own directory.

if [ -n "$1" ]; then
  DIRECTORY="$1"
else
  DIRECTORY=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
fi

# Define an associative array for the new benchmark hashes
# These must match the "version" field in results/benchmarks.json
declare -A BENCHMARKS
BENCHMARKS["compilation.bench_example_load.SlowExampleBasicUrdf.time_load"]="c8e96aea345de87f484e4ed6e86421603d52ec779120a3fabd839464dfb51e39"
BENCHMARKS["compilation.bench_example_load.SlowExampleClothFranka.time_load"]="a6a2562647fb69702746b637db6c23fa382b05b0e97cee7afbb7ba6592a83518"
BENCHMARKS["compilation.bench_example_load.SlowExampleClothTwist.time_load"]="6b93c89629e18ae89ec3308320451db50eb83f24977a80a69f364b73d435435b"
BENCHMARKS["compilation.bench_example_load.SlowExampleRobotAnymal.time_load"]="7f67d241c037d76eccd4b56077ac053d751b82828d090cfbeb9001d0088152bc"
BENCHMARKS["compilation.bench_example_load.SlowExampleRobotCartpole.time_load"]="156564a71da0483e487b79b3529bc50e31f7281c494a48b9ca2d12300094be02"
BENCHMARKS["setup.bench_model.FastInitializeModel.peakmem_initialize_model_cpu"]="889585d54e5e70fe61ed7e1e066b837180ea8bde16da86aa735ad894f10f63f4"
BENCHMARKS["setup.bench_model.FastInitializeModel.time_initialize_model"]="2c5b54190ffe915edf4bedba6e1bda0783dd321f2141a56e52ace85061077198"
BENCHMARKS["setup.bench_model.FastInitializeSolver.time_initialize_solver"]="3b89e042bc863172b61d3d39c02f8f67dffe87664041c32c6e277846ed2095dd"
BENCHMARKS["setup.bench_model.FastInitializeViewerGL.time_initialize_renderer"]="6c957e22fbeb7711e6fbdfb6f8053bb4147d24a6d118c46438a961f3a2c8feab"
BENCHMARKS["setup.bench_model.KpiInitializeModel.time_initialize_model"]="1eb1943d31536b040079c24c6428a73a866fdab4411562e31dbf0c79bcb18df9"
BENCHMARKS["setup.bench_model.KpiInitializeSolver.time_initialize_solver"]="e358228dda3fc4e02785210c91dce733b1d1aebbce52f3d3ac0dedf2827160a3"
BENCHMARKS["setup.bench_model.KpiInitializeViewerGL.time_initialize_renderer"]="5ba06d80fcf8716093a193bd47034b063820abddda6df221a0f5d2df380f8e01"
BENCHMARKS["simulation.bench_anymal.FastExampleAnymalPretrained.time_simulate"]="3a10c8d05e3cc6621a9079cbdf32b3673985f39e1c6823561b2d025c878dec3b"
BENCHMARKS["simulation.bench_cable.FastExampleCablePile.time_simulate"]="38579de24aa1852dd217c842dc29042fe4671b747fb616437af39fb2e8604988"
BENCHMARKS["simulation.bench_cloth.FastExampleClothManipulation.time_simulate"]="1369873c0a88c16d3821097693638b7a5a3586fdfb9a79f8664f39368d529c73"
BENCHMARKS["simulation.bench_cloth.FastExampleClothTwist.time_simulate"]="4550069ca84ba0bd50f608a46dad4a7d29ab17d08b7bed62ceea9f55e1c73ee0"
BENCHMARKS["simulation.bench_contacts.FastExampleContactHydroWorkingDefaults.time_simulate"]="5389daa5fed1f5449fafa713a96cfc36b7e954e6fc823937abc43fcfb2f12c37"
BENCHMARKS["simulation.bench_contacts.FastExampleContactPyramidDefaults.time_simulate"]="5b2a5503945a50c99a14b5e5ff6eeba0b8ec8251d67bf4de83b53e82fd7b5388"
BENCHMARKS["simulation.bench_contacts.FastExampleContactSdfDefaults.time_simulate"]="75fa33f2d98e88de35f707645ccb9f5c5366ca83ed131b9f85b51bc872a30f16"
BENCHMARKS["simulation.bench_cpu.CpuIKFranka.time_solve"]="9fcf20853dc25c179cf22edc84aaecfbc94de82b1f4b033cce852ac472cd553c"
BENCHMARKS["simulation.bench_cpu.CpuMuJoCoAnt.time_simulate"]="0a22cae57e12fedfe0c13401c99f74103930eddc22cb682f7ea0c645fea34fab"
BENCHMARKS["simulation.bench_cpu.CpuXPBDQuadruped.time_simulate"]="54b6dd283508ea5212d65e1e09425583d291e6a060bd4cfa3e7626e86079f450"
# HeightfieldCollision: hash refreshed by newton #3409 (44cb76b1, 2026-07-20,
# removes model.collide usage); values continuous at the boundary -> merged 2026-07-24.
BENCHMARKS["simulation.bench_heightfield.HeightfieldCollision.time_simulate"]="8e299acd5d4ec1c57041096396508170a9e8e52acd78cf3a3efb16387d047b33"
BENCHMARKS["simulation.bench_ik.FastIKSolve.time_solve"]="e00213950917f07ae44e3e993493cfcb1730b7eaba5277047565a289f98c1f73"
# FastInverseDynamics: history merged across newton #3530 (2026-07-16 rename
# time_eval_inverse_dynamics -> _passive + _force source refresh; timed regions
# unchanged, no boundary step on any crossed machine/env). Old keys were renamed
# in historical result files; old hashes 91509c0a/f1893d5d rewritten below.
BENCHMARKS["simulation.bench_inverse_dynamics.FastInverseDynamics.time_eval_inverse_dynamics_passive"]="f30af9c4867af17886ff758d055b4a5325385e407a8a2465b1d577e8e0ca47c7"
BENCHMARKS["simulation.bench_inverse_dynamics.FastInverseDynamics.time_eval_inverse_dynamics_force"]="9f1873a9ea3ce3d13d0a7cff5fe4c94cdaa60c47690cd182fc63ff4216688119"
BENCHMARKS["simulation.bench_kamino.FastDRLegs.time_simulate"]="5e87eea3aa3c9a5607ca7796ab168be681dfa2a8519b8461e812d378d06f77bb"
BENCHMARKS["simulation.bench_kamino.KpiDRLegs.track_simulate"]="6afbd53709aa79872d11287096428c71195e4269b17e855c9cb6ddc643ad90a4"
# NotifyDRLegs: hashes refreshed by newton #3566 (2026-07-22); boundary-continuous
# series merged 2026-07-24. time_notify_shape_properties DEFERRED (not merged):
# coherent +13-19% at the boundary on both SC-PV py3.12 envs with a single
# pre-boundary point -- revisit once more post-#3566 data exists.
BENCHMARKS["simulation.bench_kamino.NotifyDRLegs.time_notify_actuator_properties"]="8b301f560e11839f31d6855ae626ebc757f5b4c4decf0b942add5c3113108d97"
BENCHMARKS["simulation.bench_kamino.NotifyDRLegs.time_notify_all"]="4aa876370ee3a7e0e3306ab7bb2fe64ff09cee31fb7f2e14b99cbe0b8f592023"
BENCHMARKS["simulation.bench_kamino.NotifyDRLegs.time_notify_body_inertial_properties"]="17683f4fb9f561706d45681687c5b601141badee8cecf8837564f7688e98924e"
BENCHMARKS["simulation.bench_kamino.NotifyDRLegs.time_notify_body_properties"]="d6e765a8d6a228d6bcab6dbde46120f256cf81b8762ae5426d865fffb7f506e9"
BENCHMARKS["simulation.bench_kamino.NotifyDRLegs.time_notify_joint_dof_properties"]="68a5c53fa57388b2500caa6f6710410ea90f5a2e88e2b0faed2c6f19577973eb"
BENCHMARKS["simulation.bench_kamino.NotifyDRLegs.time_notify_joint_properties"]="76973bd6ed3808865065738b8f677887e791e794eba1108aece0290c07ca2768"
BENCHMARKS["simulation.bench_kamino.NotifyDRLegs.time_notify_model_properties"]="a00bd83135d32a2d8a2f0b12c013bedd3fe78deca191fa260e6bff6ad02b0cd6"
# bench_mujoco Fast*/NewtonOverhead* + kamino/anymal/quadruped_xpbd entries updated
# 2026-07-24: history merged across newton #3566 (a051c39a, metrics refresh) and
# #3575 (38c44beb, stock solver iterations); per-series boundary continuity verified.
BENCHMARKS["simulation.bench_mujoco.FastAllegro.track_simulate"]="f274c5b16ed3364e061b34647449d68927d90ee8745741587e496620c940f7b9"
BENCHMARKS["simulation.bench_mujoco.FastCartpole.track_simulate"]="8a800c46570dc8f80a53c8c5d6ee5a40f026717d956789815d2ae13f1fce0c4e"
BENCHMARKS["simulation.bench_mujoco.FastG1.track_simulate"]="af2357cbb67a326409520acf9acba3879713122bcca0c4f04a2c4fa1cbc018a8"
BENCHMARKS["simulation.bench_mujoco.FastHumanoid.track_simulate"]="7022153f0c8e8a37e16f036d8763c852d238e5f33b4c69c6b4e0c70cac342993"
# simulation.bench_mujoco.FastKitchenG1.track_simulate: intentionally NOT
# merged across newton #3566 (2026-07-22): benchmark bumped to version="2"
# because the pre-v2 series accidentally omitted the kitchen environment.
# Old series ends there; v2 starts fresh (~2x slower, first correct numbers).
# Decision: Dylan Turpin (#newton-dev, 2026-07-24). Precedent: tiled-camera #3480.
BENCHMARKS["simulation.bench_mujoco.FastNewtonOverheadG1.track_simulate"]="215e4ca892e1f954f5a3a010d9514c07b1da5a5285136bf0bb480950c2efc7f5"
BENCHMARKS["simulation.bench_mujoco.FastNewtonOverheadHumanoid.track_simulate"]="215e4ca892e1f954f5a3a010d9514c07b1da5a5285136bf0bb480950c2efc7f5"
# RealtimeHumanoidPhysics: hashes refreshed by newton #3566; values continuous -> merged 2026-07-24.
BENCHMARKS["simulation.bench_mujoco.RealtimeHumanoidPhysics.track_mean_step_ms"]="834dbf7ddd07e2ee8cb0132e432418b7d2ef01ee9d92d045f47f42ad4c79e51e"
BENCHMARKS["simulation.bench_mujoco.RealtimeHumanoidPhysics.track_p95_step_ms"]="3a6a0587470ff165281a4928f74146813770f8edc2a1bc79397f9672947916a4"
BENCHMARKS["simulation.bench_mujoco.RealtimeHumanoidPhysics.track_real_time_factor"]="f9d0be62fd656258f44bc543d17c384d9a0a4c33ea6099293f1613d2a6ad0d68"
BENCHMARKS["simulation.bench_mujoco.RealtimeHumanoidPhysics.track_step_rate_hz"]="adaa1efa3417c470503555e00ef9b80089ae1da56ee3347ec5c437bec8abe6b5"
BENCHMARKS["simulation.bench_mujoco.RealtimeHumanoidPhysics.track_step_time_cv_pct"]="3245e6ff25929dec5451ae9c766fb854562b43fc4f84bd1003c2bb1001550a25"
BENCHMARKS["simulation.bench_quadruped_xpbd.FastExampleQuadrupedXPBD.time_simulate"]="a6f219d8eb15875bdebd417e35d547a0c058bc1a75b0f9b2a919cab36c033b22"
BENCHMARKS["simulation.bench_selection.FastExampleSelectionCartpoleMuJoCo.time_simulate"]="1d5ae94d0fbd9942b54483081a9ad25b2e28122d1c6749b38c297816aa125377"
# simulation.bench_sensor_tiled_camera.*: intentionally NOT merged across the
# 2026-07-14 rework (newton #3480: new scenes, renamed classes/methods, ~4x level
# shift). Old FastSensorTiledCamera.time_rendering_pixel_priority_* history ends
# there; the new time_render_* series start fresh. Decision: Alain Denzler
# (Slack, 2026-07-16), recorded 2026-07-18.
BENCHMARKS["simulation.bench_viewer.FastViewerGL.time_rendering_frame"]="dc458e762bf26467d1e2af3f425b70413cb7675f9a0d646c652bad3d5bf4a670"
BENCHMARKS["simulation.bench_viewer.KpiViewerGL.time_rendering_frame"]="c25efe60406065ad84bde4908e8f914997f231cfbc4213475b4da9d20809bd87"

# Loop over benchmarks and get their hashes
for BENCHMARK_NAME in "${!BENCHMARKS[@]}"; do
  NEW_HASH="${BENCHMARKS[$BENCHMARK_NAME]}"

  # Escape dots in benchmark name for sed
  ESCAPED_BENCHMARK=$(echo "$BENCHMARK_NAME" | sed 's/\./\\./g')

  # Count files to process
  FILE_COUNT=$(find "$DIRECTORY" -name "*.json" -type f | wc -l)

  if [ "$FILE_COUNT" -eq 0 ]; then
    echo "Error: No JSON files found in $DIRECTORY"
    exit 1
  fi

  echo "Processing $FILE_COUNT JSON files in: $DIRECTORY"
  echo "Benchmark: $BENCHMARK_NAME"
  echo "New hash: $NEW_HASH"
  echo ""

  # Find and replace in all JSON files
  find "$DIRECTORY" -name "*.json" -type f -exec perl -0777 -pi -e 's/("'"$ESCAPED_BENCHMARK"'": .*?)"[a-f0-9]{64}"/$1"'"$NEW_HASH"'"/xgs' {} \;
done
