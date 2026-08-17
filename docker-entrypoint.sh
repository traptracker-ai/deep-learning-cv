#!/bin/bash
# ============================================================
# Container entrypoint
# Starts JupyterLab in the background and the launcher in the foreground.
# The launcher is the single entry point students hit at http://localhost:8000.
# ============================================================
set -euo pipefail

JUPYTER_TOKEN="${JUPYTER_TOKEN:-deep-learning-cv}"

echo "================================================================"
echo " Deep Learning — module container"
echo "================================================================"
echo " Launcher:   http://localhost:8000"
echo " JupyterLab: http://localhost:8888  (token: ${JUPYTER_TOKEN})"
echo "================================================================"

# --- Start JupyterLab in the background ---
cd /workspace
jupyter lab \
    --ip=0.0.0.0 \
    --port=8888 \
    --no-browser \
    --ServerApp.token="${JUPYTER_TOKEN}" \
    --ServerApp.password='' \
    --ServerApp.root_dir=/workspace \
    --ServerApp.allow_origin='*' \
    --ServerApp.disable_check_xsrf=True \
    > /tmp/jupyter.log 2>&1 &
JUPYTER_PID=$!

# Give Jupyter a moment to come up before the launcher starts linking to it.
sleep 2

# --- Start the launcher in the foreground ---
# JUPYTER_TOKEN is read by the launcher so it can generate working notebook URLs.
export JUPYTER_TOKEN
exec python -m flask --app launcher/app.py run --host=0.0.0.0 --port=8000
