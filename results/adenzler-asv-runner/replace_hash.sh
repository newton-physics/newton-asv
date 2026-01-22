#!/bin/bash

# Get the directory of the script
DIRECTORY=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Define an associative array for the new benchmark hashes
declare -A BENCHMARKS
BENCHMARKS["compilation.bench_example_load.SlowExampleBasicUrdf.time_load"]="5212ba785a2d013b8fc4b4fd1f0281ba23f65a10036f337e6abebdcd1784a35a"
BENCHMARKS["compilation.bench_example_load.SlowExampleClothFranka.time_load"]="9a1d510bf84d0d2d4d3c68dc0b43f672866854e51df5b70071be0cc9a9aa37ee"
BENCHMARKS["compilation.bench_example_load.SlowExampleClothTwist.time_load"]="2944bcd1d41a1d0755a46fab1ccbb2b38418c589a0ebb982702ba9be5bd32471"
BENCHMARKS["compilation.bench_example_load.SlowExampleRobotAnymal.time_load"]="30b4e830fd859608ff412e9052e49492eb804327e44f3cbedf4183876c171021"
BENCHMARKS["compilation.bench_example_load.SlowExampleRobotCartpole.time_load"]="71e2c9a9b0957497094f25a0b4dff3546059e17c249880ccff2c5a3dc09debf7"
BENCHMARKS["compilation.bench_example_load.SlowExampleRobotHumanoid.time_load"]="3d838883c58af639755f7dcfa6d7b6f603f4faefa35577421e70a41be5877518"
BENCHMARKS["setup.bench_model.FastInitializeModel.peakmem_initialize_model_cpu"]="27442c181e1ed8ac16c6cf2cdba2e06b04ed98f319b287d1c31cae587b352eb3"
BENCHMARKS["setup.bench_model.FastInitializeModel.time_initialize_model"]="4a37efc34b9e8d64a37f778ed2f2874065a56dd0f2a0798b16e5f6cafdc4bf88"
BENCHMARKS["setup.bench_model.FastInitializeSolver.time_initialize_solver"]="b2d1b17d4e4a010a2441d0d10b9b209c4884c57db6d16b718c8c9b5127f838a1"
BENCHMARKS["setup.bench_model.FastInitializeViewerGL.time_initialize_renderer"]="d9add5c09316bc748c3e612cc16cbd7f095ec18b01a1b27b1ea8e239cab0b94a"
BENCHMARKS["setup.bench_model.KpiInitializeModel.time_initialize_model"]="53272b20ee0eacff6fdbc0e21ce8b18aab7e4201a123fc59bc4606b6de60b08d"
BENCHMARKS["setup.bench_model.KpiInitializeSolver.time_initialize_solver"]="55e5ec342e9efdcb797c22fdcf5d25b898c00a14c8edbbaf90a3858b53683d50"
BENCHMARKS["setup.bench_model.KpiInitializeViewerGL.time_initialize_renderer"]="2d33b796bb69aafb93c3c88f9a12b13808e8a5cdb6df7562ded097818f80b51c"
BENCHMARKS["simulation.bench_anymal.FastExampleAnymalPretrained.time_simulate"]="29d871d361f5e50619ca9ee4af8ee5f22def523c03a5aa19b0365c23ecb5dd28"
BENCHMARKS["simulation.bench_cloth.FastExampleClothManipulation.time_simulate"]="b3ceadbc55945ff4c6130a4fbcec6e455edc4e3085dd62f0e02103dbd33101ad"
BENCHMARKS["simulation.bench_cloth.FastExampleClothTwist.time_simulate"]="01dfa4b62b6e71ea72ece4c0c2371d26b1ba72a8ef8c94a900d8e40be3907293"
BENCHMARKS["simulation.bench_mujoco.FastAllegro.time_simulate"]="98b9f7c46ab706d7f678e15627289fc532818b22d5fe7bf529ff7d54cb640a50"
BENCHMARKS["simulation.bench_mujoco.FastCartpole.time_simulate"]="98b9f7c46ab706d7f678e15627289fc532818b22d5fe7bf529ff7d54cb640a50"
BENCHMARKS["simulation.bench_mujoco.FastG1.time_simulate"]="98b9f7c46ab706d7f678e15627289fc532818b22d5fe7bf529ff7d54cb640a50"
BENCHMARKS["simulation.bench_mujoco.FastHumanoid.time_simulate"]="98b9f7c46ab706d7f678e15627289fc532818b22d5fe7bf529ff7d54cb640a50"
BENCHMARKS["simulation.bench_mujoco.FastKitchenG1.time_simulate"]="98b9f7c46ab706d7f678e15627289fc532818b22d5fe7bf529ff7d54cb640a50"
BENCHMARKS["simulation.bench_mujoco.KpiAllegro.track_simulate"]="62a2fd707ff553505c8e26bae864c53867d55fc0442b3c6429ccc112ee6b21ad"
BENCHMARKS["simulation.bench_mujoco.KpiCartpole.track_simulate"]="62a2fd707ff553505c8e26bae864c53867d55fc0442b3c6429ccc112ee6b21ad"
BENCHMARKS["simulation.bench_mujoco.KpiG1.track_simulate"]="62a2fd707ff553505c8e26bae864c53867d55fc0442b3c6429ccc112ee6b21ad"
BENCHMARKS["simulation.bench_mujoco.KpiHumanoid.track_simulate"]="62a2fd707ff553505c8e26bae864c53867d55fc0442b3c6429ccc112ee6b21ad"
BENCHMARKS["simulation.bench_mujoco.KpiKitchenG1.track_simulate"]="62a2fd707ff553505c8e26bae864c53867d55fc0442b3c6429ccc112ee6b21ad"
BENCHMARKS["simulation.bench_quadruped_xpbd.FastExampleQuadrupedXPBD.time_simulate"]="8527e31e794cfba679aafd4d750232df62492b0b836ab15cdad57ab6c92db2dc"
BENCHMARKS["simulation.bench_selection.FastExampleSelectionCartpoleMuJoCo.time_simulate"]="adc93f1285ec796ed3088445a10636624dd2a89b99b5c90bcbb42add8c9087df"
BENCHMARKS["simulation.bench_viewer.FastViewerGL.time_rendering_frame"]="a7320c2bfd979f20a9efbe3c6bcb6cbe8daf027c03fbeea90667301702873854"
BENCHMARKS["simulation.bench_viewer.KpiViewerGL.time_rendering_frame"]="9705f69f1cdc6900bdaef46555562d3ad19312423237a52028f380687c7c359d"
BENCHMARKS["simulation.bench_sensor_tiled_camera.SensorTiledCameraBenchmark.time_rendering_pixel"]="db6e545007dff185d4d73a89ad888197bfef72cc3d7afbda2e757e18dd0c797b"
BENCHMARKS["simulation.bench_sensor_tiled_camera.SensorTiledCameraBenchmark.time_rendering_tiled"]="89c041db2e6d633fe775ee5a3cd438c5babb643e7a99baba48227ad0f4a071cf"

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
  #find "$DIRECTORY" -name "*.json" -type f -exec perl -i -pe "s/(\"$ESCAPED_BENCHMARK\": .*?), \"[a-f0-9]{64}\"/\$1, \"$NEW_HASH\"/" {} \;
done
