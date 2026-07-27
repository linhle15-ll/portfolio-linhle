#!/bin/bash

tmux kill-server 2>/dev/null || true

cd ~/portfolio-linhle

git fetch && git reset origin/main --hard

source python3-virtualvenv/bin/activate
pip install -r requirements.txt

# 5. Restart Docker containers (MySQL etc.)
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build

# tmux new-session -d -s portfolio -c ~/portfolio-linhle \; send-keys "source python3-virtualvenv/bin/activate && flask run --host=0.0.0.0 --port=5000" Enter
# using systemd instead of tmux
# Restart Flask via systemd
systemctl daemon-reload
systemctl restart myportfolio
systemctl status myportfolio

echo "Done! Flask is running at http://linhthechef.duckdns.org:5000"
