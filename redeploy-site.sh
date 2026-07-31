#!/bin/bash

# 1. Kill any leftover tmux sessions
tmux kill-server 2>/dev/null || true

# 2. Go to project folder
cd ~/portfolio-linhle

# 3. Pull latest from GitHub
git fetch && git reset origin/main --hard

# Use Python environment defined in the Dockerfile (not the virtualenv on the host machine)
# source python3-virtualvenv/bin/activate
# pip install -r requirements.txt

# 4. Restart Docker containers
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build

# tmux new-session -d -s portfolio -c ~/portfolio-linhle \; send-keys "source python3-virtualvenv/bin/activate && flask run --host=0.0.0.0 --port=5000" Enter
# using systemd instead of tmux
# Restart Flask via systemd - Disabled since using Docker 
# systemctl daemon-reload
# systemctl restart myportfolio
# systemctl status myportfolio

echo "Done! Flask is running at http://linhthechef.duckdns.org:5001"
