#!/bin/bash
cd /home/ubuntu/app
pkill -f "python3 app.py" || true
nohup python3 app.py > app.log 2>&1 &
