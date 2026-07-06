#!/bin/bash

tmux kill-server 2>/dev/null || true

cd ~/portfolio-linhle

git fetch && git reset origin/main --hard

source python3-virtualvenv/bin/activate
pip install -r requirements.txt

tmux new-session -d -s portfolio -c ~/portfolio-linhle \; send-keys "source python3-virtualvenv/bin/activate && flask run --host=0.0.0.0 --port=5000" Enter

echo "Done! Flask is running at http://linhthechef.duckdns.org:5000"
