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
BENCHMARKS["compilation.bench_example_load.SlowExampleBasicUrdf.time_load"]="5212ba785a2d013b8fc4b4fd1f0281ba23f65a10036f337e6abebdcd1784a35a"
BENCHMARKS["compilation.bench_example_load.SlowExampleClothFranka.time_load"]="9a1d510bf84d0d2d4d3c68dc0b43f672866854e51df5b70071be0cc9a9aa37ee"
BENCHMARKS["compilation.bench_example_load.SlowExampleClothTwist.time_load"]="2944bcd1d41a1d0755a46fab1ccbb2b38418c589a0ebb982702ba9be5bd32471"
BENCHMARKS["compilation.bench_example_load.SlowExampleRobotAnymal.time_load"]="30b4e830fd859608ff412e9052e49492eb804327e44f3cbedf4183876c171021"
BENCHMARKS["compilation.bench_example_load.SlowExampleRobotCartpole.time_load"]="71e2c9a9b0957497094f25a0b4dff3546059e17c249880ccff2c5a3dc09debf7"
BENCHMARKS["compilation.bench_example_load.SlowExampleRobotHumanoid.time_load"]="3d838883c58af639755f7dcfa6d7b6f603f4faefa35577421e70a41be5877518"
BENCHMARKS["setup.bench_model.FastInitializeModel.peakmem_initialize_model_cpu"]="642ffc84509c186e6530cb17a6441701287ee3dac455b6d51624f5ce68535404"
BENCHMARKS["setup.bench_model.FastInitializeModel.time_initialize_model"]="8a2f444deb1bc9001cb7014bff52e797ef385358333ee5091e02f65ee018e2a5"
BENCHMARKS["setup.bench_model.FastInitializeSolver.time_initialize_solver"]="3b89e042bc863172b61d3d39c02f8f67dffe87664041c32c6e277846ed2095dd"
BENCHMARKS["setup.bench_model.FastInitializeViewerGL.time_initialize_renderer"]="6c957e22fbeb7711e6fbdfb6f8053bb4147d24a6d118c46438a961f3a2c8feab"
BENCHMARKS["setup.bench_model.KpiInitializeModel.time_initialize_model"]="2e362decc4185c828ef6d98fe6af1efffd5f87ce0cdc1bc3b377e663eb8118ee"
BENCHMARKS["setup.bench_model.KpiInitializeSolver.time_initialize_solver"]="e358228dda3fc4e02785210c91dce733b1d1aebbce52f3d3ac0dedf2827160a3"
BENCHMARKS["setup.bench_model.KpiInitializeViewerGL.time_initialize_renderer"]="5ba06d80fcf8716093a193bd47034b063820abddda6df221a0f5d2df380f8e01"
BENCHMARKS["simulation.bench_anymal.FastExampleAnymalPretrained.time_simulate"]="29d871d361f5e50619ca9ee4af8ee5f22def523c03a5aa19b0365c23ecb5dd28"
BENCHMARKS["simulation.bench_cable.FastExampleCablePile.time_simulate"]="e260055b3cc91e01feb28cdb0ea0be9d4213890d0e86785a0496fe16e5001d93"
BENCHMARKS["simulation.bench_cloth.FastExampleClothManipulation.time_simulate"]="b3ceadbc55945ff4c6130a4fbcec6e455edc4e3085dd62f0e02103dbd33101ad"
BENCHMARKS["simulation.bench_cloth.FastExampleClothTwist.time_simulate"]="01dfa4b62b6e71ea72ece4c0c2371d26b1ba72a8ef8c94a900d8e40be3907293"
BENCHMARKS["simulation.bench_contacts.FastExampleContactHydroWorkingDefaults.time_simulate"]="6158d187b22c47fcf78118159785fc13a931bcf83dfedee595b09111099e656c"
BENCHMARKS["simulation.bench_contacts.FastExampleContactSdfDefaults.time_simulate"]="04f841929f505d5e44ada951c17e465fa460263de825dad7702c8c0e14c9d4ae"
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
BENCHMARKS["simulation.bench_quadruped_xpbd.FastExampleQuadrupedXPBD.time_simulate"]="8527e31e794cfba679aafd4d750232df62492b0b836ab15cdad57ab6c92db2dc"
BENCHMARKS["simulation.bench_selection.FastExampleSelectionCartpoleMuJoCo.time_simulate"]="bf251c9421a2283e5252a8d1ad0dbd619b84bed1cb1cf7d440edc25a8dbb1b07"
BENCHMARKS["simulation.bench_sensor_tiled_camera.SensorTiledCameraBenchmark.time_rendering_pixel"]="adcb7f64f0901ab7a33483d3610daebf9d3213f7e9d33a4864f7627140169a22"
BENCHMARKS["simulation.bench_sensor_tiled_camera.SensorTiledCameraBenchmark.time_rendering_tiled"]="426c5a376da5cf4d8c4dcc24d344690403238beea87567c24c3fd5fb67f289d1"
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
