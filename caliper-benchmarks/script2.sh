docker-compose --f /storage-6T/pooja/caliper/caliper-benchmarks/networks/ethereum/1node-clique/docker-compose.yml up -d
wait
npx caliper launch manager     --caliper-workspace .     --caliper-benchconfig benchmarks/scenario/NotarySc/config.yaml     --caliper-networkconfig networks/ethereum/1node-clique/networkconfig.json
wait
npx caliper launch manager     --caliper-workspace .     --caliper-benchconfig benchmarks/scenario/NotarySc/config1.yaml     --caliper-networkconfig networks/ethereum/1node-clique/networkconfig.json
wait
npx caliper launch manager     --caliper-workspace .     --caliper-benchconfig benchmarks/scenario/NotarySc/config2.yaml     --caliper-networkconfig networks/ethereum/1node-clique/networkconfig.json
wait
npx caliper launch manager     --caliper-workspace .     --caliper-benchconfig benchmarks/scenario/NotarySc/config3.yaml     --caliper-networkconfig networks/ethereum/1node-clique/networkconfig.json
wait
npx caliper launch manager     --caliper-workspace .     --caliper-benchconfig benchmarks/scenario/NotarySc/config4.yaml     --caliper-networkconfig networks/ethereum/1node-clique/networkconfig.json
wait
npx caliper launch manager     --caliper-workspace .     --caliper-benchconfig benchmarks/scenario/NotarySc/config5.yaml     --caliper-networkconfig networks/ethereum/1node-clique/networkconfig.json
wait
npx caliper launch manager     --caliper-workspace .     --caliper-benchconfig benchmarks/scenario/NotarySc/config6.yaml     --caliper-networkconfig networks/ethereum/1node-clique/networkconfig.json
wait
npx caliper launch manager     --caliper-workspace .     --caliper-benchconfig benchmarks/scenario/NotarySc/config7.yaml     --caliper-networkconfig networks/ethereum/1node-clique/networkconfig.json
wait
npx caliper launch manager     --caliper-workspace .     --caliper-benchconfig benchmarks/scenario/NotarySc/config8.yaml     --caliper-networkconfig networks/ethereum/1node-clique/networkconfig.json
wait
npx caliper launch manager     --caliper-workspace .     --caliper-benchconfig benchmarks/scenario/NotarySc/config9.yaml     --caliper-networkconfig networks/ethereum/1node-clique/networkconfig.json
wait
docker-compose --f /storage-6T/pooja/caliper/caliper-benchmarks/networks/ethereum/1node-clique/docker-compose.yml down
wait
echo y | docker system prune -a
wait



