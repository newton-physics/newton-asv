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
BENCHMARKS["setup.bench_model.FastInitializeModel.peakmem_initialize_model_cpu"]="642ffc84509c186e6530cb17a6441701287ee3dac455b6d51624f5ce68535404"
BENCHMARKS["setup.bench_model.FastInitializeModel.time_initialize_model"]="8a2f444deb1bc9001cb7014bff52e797ef385358333ee5091e02f65ee018e2a5"
BENCHMARKS["setup.bench_model.FastInitializeSolver.time_initialize_solver"]="3b89e042bc863172b61d3d39c02f8f67dffe87664041c32c6e277846ed2095dd"
BENCHMARKS["setup.bench_model.FastInitializeViewerGL.time_initialize_renderer"]="6c957e22fbeb7711e6fbdfb6f8053bb4147d24a6d118c46438a961f3a2c8feab"
BENCHMARKS["setup.bench_model.KpiInitializeModel.time_initialize_model"]="2e362decc4185c828ef6d98fe6af1efffd5f87ce0cdc1bc3b377e663eb8118ee"
BENCHMARKS["setup.bench_model.KpiInitializeSolver.time_initialize_solver"]="e358228dda3fc4e02785210c91dce733b1d1aebbce52f3d3ac0dedf2827160a3"
BENCHMARKS["setup.bench_model.KpiInitializeViewerGL.time_initialize_renderer"]="5ba06d80fcf8716093a193bd47034b063820abddda6df221a0f5d2df380f8e01"
BENCHMARKS["simulation.bench_anymal.FastExampleAnymalPretrained.time_simulate"]="75c29742e27150b74bf2fb9266a43bc095106bfc7a54ed4028f5275c88311b78"
BENCHMARKS["simulation.bench_cable.FastExampleCablePile.time_simulate"]="6bb980a7c23aac4938375cc136c10fae422fdb9204b4f94170f3a94a15e85e0b"
BENCHMARKS["simulation.bench_cloth.FastExampleClothManipulation.time_simulate"]="1369873c0a88c16d3821097693638b7a5a3586fdfb9a79f8664f39368d529c73"
BENCHMARKS["simulation.bench_cloth.FastExampleClothTwist.time_simulate"]="4550069ca84ba0bd50f608a46dad4a7d29ab17d08b7bed62ceea9f55e1c73ee0"
BENCHMARKS["simulation.bench_contacts.FastExampleContactHydroWorkingDefaults.time_simulate"]="5389daa5fed1f5449fafa713a96cfc36b7e954e6fc823937abc43fcfb2f12c37"
BENCHMARKS["simulation.bench_contacts.FastExampleContactPyramidDefaults.time_simulate"]="5b2a5503945a50c99a14b5e5ff6eeba0b8ec8251d67bf4de83b53e82fd7b5388"
BENCHMARKS["simulation.bench_contacts.FastExampleContactSdfDefaults.time_simulate"]="75fa33f2d98e88de35f707645ccb9f5c5366ca83ed131b9f85b51bc872a30f16"
BENCHMARKS["simulation.bench_heightfield.HeightfieldCollision.time_simulate"]="0f0cb2b6870d03f27c8e3aedf780b4b30b7fb49c4afd4e06d9c3c58f8a4f9760"
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
BENCHMARKS["simulation.bench_sensor_contact.InitSensorContact.time_total_only"]="e27f2633bca589773c0585d5c83561db134bb2cf90311eefef8366ead76797d7"
BENCHMARKS["simulation.bench_sensor_contact.InitSensorContact.time_with_counterparts"]="e5c4025e446be1d8637bc31e165be8868a291cbc61efcc13d1db62f07395f13c"
BENCHMARKS["simulation.bench_sensor_contact.InitSensorContactWithMatching.time_total_only"]="ad7784872812f0e2a28c9aad3b4a19919c463e15bcb9116e872c6465899befcd"
BENCHMARKS["simulation.bench_sensor_contact.InitSensorContactWithMatching.time_with_counterparts"]="63339109b81fd87bf13fe73e96a3f1040ddfe6fcc6e1f3451d673d26db18a647"
BENCHMARKS["simulation.bench_sensor_contact.UpdateSensorContact.time_total_only"]="92981e33eb35e2e11fd52219859e984c635fbb0fd9956424a3c359b554101525"
BENCHMARKS["simulation.bench_sensor_contact.UpdateSensorContact.time_with_counterparts"]="fe93d00afc005f6922b82974903d1459e3adae68561c4b73fa956afb896a6c6b"
BENCHMARKS["simulation.bench_sensor_tiled_camera.SensorTiledCameraBenchmark.time_rendering_pixel"]="adcb7f64f0901ab7a33483d3610daebf9d3213f7e9d33a4864f7627140169a22"
BENCHMARKS["simulation.bench_sensor_tiled_camera.SensorTiledCameraBenchmark.time_rendering_pixel_priority_color_depth"]="c096eaed75395a3dc9b3141f8cb13b900bc77facbb91f869015fcc7af5ff4144"
BENCHMARKS["simulation.bench_sensor_tiled_camera.SensorTiledCameraBenchmark.time_rendering_pixel_priority_color_only"]="33b8449fb693f90fbcb989be1476fba70d0163b342b6ee3d0a44e2d71452963a"
BENCHMARKS["simulation.bench_sensor_tiled_camera.SensorTiledCameraBenchmark.time_rendering_pixel_priority_depth_only"]="a59842efad26ee8bcae4e66cb84d25d35bbd0ea03eedfe32a460cfccd5c9ccce"
BENCHMARKS["simulation.bench_sensor_tiled_camera.SensorTiledCameraBenchmark.time_rendering_tiled"]="426c5a376da5cf4d8c4dcc24d344690403238beea87567c24c3fd5fb67f289d1"
BENCHMARKS["simulation.bench_sensor_tiled_camera.SensorTiledCameraBenchmark.time_rendering_tiled_color_depth"]="48f640b1f9b9dab0387c27b4520a0f04512b7492e4e6756f2d8c1e61a2d5fb46"
BENCHMARKS["simulation.bench_sensor_tiled_camera.SensorTiledCameraBenchmark.time_rendering_tiled_color_only"]="ca06d74493d97b5f106d942780108ea3b66890486fe6d86001f5471ee18cb320"
BENCHMARKS["simulation.bench_sensor_tiled_camera.SensorTiledCameraBenchmark.time_rendering_tiled_depth_only"]="bd66313efe10bd94f962ac429ab5a91ca390ed9549bd08d8639abbea18695348"
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
