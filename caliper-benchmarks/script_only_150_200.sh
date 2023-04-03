
wait
npx caliper launch manager  --caliper-workspace .  --caliper-benchconfig benchmarks/scenario/registerSc/config_ret_200.yaml  --caliper-networkconfig networks/ethereum/1node-clique/networkconfig.json
wait
mv report.html report_200_5.html
wait
npx caliper launch manager  --caliper-workspace .  --caliper-benchconfig benchmarks/scenario/registerSc/config_ret_200.yaml  --caliper-networkconfig networks/ethereum/1node-clique/networkconfig.json
wait
mv report.html report_200_7.html
wait
npx caliper launch manager  --caliper-workspace .  --caliper-benchconfig benchmarks/scenario/registerSc/config_ret_200.yaml  --caliper-networkconfig networks/ethereum/1node-clique/networkconfig.json
wait
mv report.html report_200_8.html
