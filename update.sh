#!/bin/bash
# ボットのプロセスを安全に停止
pkill -f src/adry_discord_toolbox/main.py

# 最新のコードを取得
git pull origin main

# ボットを再起動
nohup python src/adry_discord_toolbox/main.py &
