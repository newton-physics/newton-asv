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
BENCHMARKS["setup.bench_model.FastInitializeModel.peakmem_initialize_model_cpu"]="642ffc84509c186e6530cb17a6441701287ee3dac455b6d51624f5ce68535404"
BENCHMARKS["setup.bench_model.FastInitializeModel.time_initialize_model"]="8a2f444deb1bc9001cb7014bff52e797ef385358333ee5091e02f65ee018e2a5"
BENCHMARKS["setup.bench_model.FastInitializeSolver.time_initialize_solver"]="3b89e042bc863172b61d3d39c02f8f67dffe87664041c32c6e277846ed2095dd"
BENCHMARKS["setup.bench_model.FastInitializeViewerGL.time_initialize_renderer"]="6c957e22fbeb7711e6fbdfb6f8053bb4147d24a6d118c46438a961f3a2c8feab"
BENCHMARKS["setup.bench_model.KpiInitializeModel.time_initialize_model"]="2e362decc4185c828ef6d98fe6af1efffd5f87ce0cdc1bc3b377e663eb8118ee"
BENCHMARKS["setup.bench_model.KpiInitializeSolver.time_initialize_solver"]="e358228dda3fc4e02785210c91dce733b1d1aebbce52f3d3ac0dedf2827160a3"
BENCHMARKS["setup.bench_model.KpiInitializeViewerGL.time_initialize_renderer"]="5ba06d80fcf8716093a193bd47034b063820abddda6df221a0f5d2df380f8e01"
BENCHMARKS["setup.bench_sdf.FastBuildSdf.time_build_sdf"]="81cad18658401245950ccf41b0a34a9b572e60b0a25eecc4a92ad561c5e09426"
BENCHMARKS["simulation.bench_anymal.FastExampleAnymalPretrained.time_simulate"]="75c29742e27150b74bf2fb9266a43bc095106bfc7a54ed4028f5275c88311b78"
BENCHMARKS["simulation.bench_cable.FastExampleCablePile.time_simulate"]="38579de24aa1852dd217c842dc29042fe4671b747fb616437af39fb2e8604988"
BENCHMARKS["simulation.bench_cloth.FastExampleClothManipulation.time_simulate"]="1369873c0a88c16d3821097693638b7a5a3586fdfb9a79f8664f39368d529c73"
BENCHMARKS["simulation.bench_cloth.FastExampleClothTwist.time_simulate"]="4550069ca84ba0bd50f608a46dad4a7d29ab17d08b7bed62ceea9f55e1c73ee0"
BENCHMARKS["simulation.bench_contacts.FastExampleContactHydroWorkingDefaults.time_simulate"]="5389daa5fed1f5449fafa713a96cfc36b7e954e6fc823937abc43fcfb2f12c37"
BENCHMARKS["simulation.bench_contacts.FastExampleContactPyramidDefaults.time_simulate"]="5b2a5503945a50c99a14b5e5ff6eeba0b8ec8251d67bf4de83b53e82fd7b5388"
BENCHMARKS["simulation.bench_contacts.FastExampleContactSdfDefaults.time_simulate"]="75fa33f2d98e88de35f707645ccb9f5c5366ca83ed131b9f85b51bc872a30f16"
BENCHMARKS["simulation.bench_heightfield.HeightfieldCollision.time_simulate"]="6d62f8706ec6d05d0274666772150be21a893c0a6f051f33c06bb1f8b3c817b6"
BENCHMARKS["simulation.bench_ik.FastIKSolve.time_solve"]="e00213950917f07ae44e3e993493cfcb1730b7eaba5277047565a289f98c1f73"
BENCHMARKS["simulation.bench_mujoco.FastAllegro.time_simulate"]="a9943a47a32e58d301ee4f2414018689d4fde3b59fc43affcff294f2a21178f8"
BENCHMARKS["simulation.bench_mujoco.FastCartpole.time_simulate"]="a9943a47a32e58d301ee4f2414018689d4fde3b59fc43affcff294f2a21178f8"
BENCHMARKS["simulation.bench_mujoco.FastG1.time_simulate"]="a9943a47a32e58d301ee4f2414018689d4fde3b59fc43affcff294f2a21178f8"
BENCHMARKS["simulation.bench_mujoco.FastHumanoid.time_simulate"]="a9943a47a32e58d301ee4f2414018689d4fde3b59fc43affcff294f2a21178f8"
BENCHMARKS["simulation.bench_mujoco.FastKitchenG1.time_simulate"]="a9943a47a32e58d301ee4f2414018689d4fde3b59fc43affcff294f2a21178f8"
BENCHMARKS["simulation.bench_mujoco.FastNewtonOverheadG1.track_simulate"]="fe70e157fca3a62483a36774d09261958a0fedbf90954bc3cd3db4f230fa368d"
BENCHMARKS["simulation.bench_mujoco.FastNewtonOverheadHumanoid.track_simulate"]="fe70e157fca3a62483a36774d09261958a0fedbf90954bc3cd3db4f230fa368d"
BENCHMARKS["simulation.bench_mujoco.KpiAllegro.track_simulate"]="7deb8426115b4478e0218848034ff1ce843d79f6fa7c3eab3ae47225cea6f22a"
BENCHMARKS["simulation.bench_mujoco.KpiCartpole.track_simulate"]="7deb8426115b4478e0218848034ff1ce843d79f6fa7c3eab3ae47225cea6f22a"
BENCHMARKS["simulation.bench_mujoco.KpiG1.track_simulate"]="7deb8426115b4478e0218848034ff1ce843d79f6fa7c3eab3ae47225cea6f22a"
BENCHMARKS["simulation.bench_mujoco.KpiHumanoid.track_simulate"]="7deb8426115b4478e0218848034ff1ce843d79f6fa7c3eab3ae47225cea6f22a"
BENCHMARKS["simulation.bench_mujoco.KpiKitchenG1.track_simulate"]="7deb8426115b4478e0218848034ff1ce843d79f6fa7c3eab3ae47225cea6f22a"
BENCHMARKS["simulation.bench_mujoco.KpiNewtonOverheadG1.track_simulate"]="fe70e157fca3a62483a36774d09261958a0fedbf90954bc3cd3db4f230fa368d"
BENCHMARKS["simulation.bench_mujoco.KpiNewtonOverheadHumanoid.track_simulate"]="fe70e157fca3a62483a36774d09261958a0fedbf90954bc3cd3db4f230fa368d"
BENCHMARKS["simulation.bench_quadruped_xpbd.FastExampleQuadrupedXPBD.time_simulate"]="50d0cd3276e6b4626370aa795870defa62f275117a504676f0ca58280e23d9ac"
BENCHMARKS["simulation.bench_selection.FastExampleSelectionCartpoleMuJoCo.time_simulate"]="1d5ae94d0fbd9942b54483081a9ad25b2e28122d1c6749b38c297816aa125377"
BENCHMARKS["simulation.bench_sensor_tiled_camera.SensorTiledCameraBenchmark.time_rendering_pixel_priority_color_depth"]="939f5d1ea837a34871e950d4e7ba8788446966138cb3e37aba53b03b1c0a3706"
BENCHMARKS["simulation.bench_sensor_tiled_camera.SensorTiledCameraBenchmark.time_rendering_pixel_priority_color_only"]="2f68a7db46361225afeb0b376d95d6cc2a664a7ec8f330ecd513d695dcc1d1a6"
BENCHMARKS["simulation.bench_sensor_tiled_camera.SensorTiledCameraBenchmark.time_rendering_pixel_priority_depth_only"]="29207d4598934b7451dbc362f1a599757265a632c4976131ac2fe2fa262b2848"
BENCHMARKS["simulation.bench_sensor_tiled_camera.SensorTiledCameraBenchmark.time_rendering_tiled_color_depth"]="c45f84375b41aec1e1178838a27a97f2fd001234cce70b66d72f59b0985aa68a"
BENCHMARKS["simulation.bench_sensor_tiled_camera.SensorTiledCameraBenchmark.time_rendering_tiled_color_only"]="45de9cd37b9ec03e270efbf324955bc3bbc86589537e2c0e07d8e4b46cd589a5"
BENCHMARKS["simulation.bench_sensor_tiled_camera.SensorTiledCameraBenchmark.time_rendering_tiled_depth_only"]="4c889221591433b7657ae56cf553c48149e2a8175d02ab5ecb072ecc7c338578"
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
