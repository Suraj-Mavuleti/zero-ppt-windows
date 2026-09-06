#!/bin/bash
# AUTO-UPDATER
cd /home/suraj/.gemini/antigravity/scratch/zero_suite/zero-ppt-windows
git pull origin main --quiet
python3 zero_ppt_gui.py
