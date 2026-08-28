#!/bin/bash
# ============================================================
# Container entrypoint
# Starts JupyterLab in the background and the launcher in the foreground.
# The launcher is the single entry point students hit at http://localhost:7144.
# ============================================================
set -euo pipefail

JUPYTER_TOKEN="${JUPYTER_TOKEN:-deep-learning-cv}"

# --- Seed an empty bind-mounted labs/ folder on first run ---
# If you pulled this image from Docker Hub and bind-mounted a fresh local
# folder onto /workspace/labs, the mount hides whatever was baked into the
# image at that path — you'd otherwise start with an empty labs/ and no
# notebooks. Populate it once from the pristine copy kept at /opt/labs-seed
# (see Dockerfile). Never touches a labs/ folder that already has content,
# so this is safe to leave in place across every later restart.
if [ -d /opt/labs-seed ] && [ -z "$(ls -A /workspace/labs 2>/dev/null)" ]; then
    echo "labs/ is empty — copying in the lab content (first run)..."
    cp -r /opt/labs-seed/. /workspace/labs/
fi

echo "================================================================"
echo " Deep Learning — module container"
echo "================================================================"
echo " Launcher:   http://localhost:7144"
echo " JupyterLab: http://localhost:7154  (token: ${JUPYTER_TOKEN})"
echo "================================================================"

# --- Start JupyterLab in the background ---
cd /workspace
jupyter lab \
    --ip=0.0.0.0 \
    --port=7154 \
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
exec python -m flask --app launcher/app.py run --host=0.0.0.0 --port=7144
