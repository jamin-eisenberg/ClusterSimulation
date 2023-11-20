git fetch --tags
latestTag=$(git describe --tags `git rev-list --tags --max-count=1`)
git checkout $latestTag
export DISPLAY=:0
python3 cluster_simulation.py