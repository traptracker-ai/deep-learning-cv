# ============================================================
# 7144COMP Deep Learning Concepts and Techniques
# Single container with all module labs and a launcher entry point.
# ============================================================
#
# Build:   docker compose build
# Run:     docker compose up
# Open:    http://localhost:8000   (launcher)
#          http://localhost:8888   (JupyterLab, if you want to bypass the launcher)
#
# ------------------------------------------------------------
# Base image
# ------------------------------------------------------------
# We use a CUDA-enabled base image so the YOLO/Ultralytics lab (Lab 7+)
# can use the GPU. Labs 1-6 don't need CUDA but still work fine in this
# environment - the only cost is image size (~10 GB vs ~3 GB for the
# slim Python base).
#
# Version notes:
#   - CUDA 12.4 + cuDNN 9 + Ubuntu 22.04: matches the requirements of
#     PyTorch 2.4+ and Ultralytics 26.x. Works with Ampere (RTX 30xx),
#     Ada (RTX 40xx), and Blackwell (RTX 50xx) consumer GPUs.
#   - We use the `devel` tag (not `runtime`) because some Python ML
#     packages still build CUDA code at install time.
# ------------------------------------------------------------

FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04 AS base

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    TZ=Etc/UTC

# ------------------------------------------------------------
# System packages
# ------------------------------------------------------------
# - python3.11 + pip: the runtime
# - build-essential: for compiled wheels
# - git, curl, ca-certificates: students fetching resources
# - libgl1, libglib2.0-0: OpenCV / image library transitive deps
# - ffmpeg: needed for YOLO's video inference path
# - tzdata: avoid prompts
RUN apt-get update && apt-get install -y --no-install-recommends \
        software-properties-common \
        ca-certificates \
        tzdata \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y --no-install-recommends \
        python3.11 \
        python3.11-venv \
        python3.11-dev \
        python3.11-distutils \
        python3-pip \
        build-essential \
        curl \
        git \
        libgl1 \
        libglib2.0-0 \
        ffmpeg \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
    && curl -fsSL https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py \
    && python3.11 /tmp/get-pip.py \
    && rm /tmp/get-pip.py \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user so students don't run notebooks as root.
ARG USERNAME=student
ARG USER_UID=1000
ARG USER_GID=1000
RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} --create-home --shell /bin/bash ${USERNAME}

WORKDIR /workspace

# ------------------------------------------------------------
# Python dependencies
# ------------------------------------------------------------
# PyTorch with CUDA support is the biggest install. We pull it from
# PyTorch's CUDA wheel index, and we MUST prevent later installs
# (especially ultralytics) from upgrading it to a PyPI build compiled
# against a newer CUDA than the host driver supports.
#
# The mechanism: a pip *constraints* file. Unlike requirements, a
# constraints file says "IF this package is installed, it must be exactly
# this version" — it doesn't install anything itself, but it caps what
# any dependency resolution is allowed to choose. So when ultralytics
# asks for torch>=1.8, pip is forced to keep our 2.4.1+cu124 build
# rather than pulling a newer CPU/cu13x wheel from PyPI.
#
# Note on `--ignore-installed blinker`: the Ubuntu CUDA base image ships
# an old `blinker` 1.4 via the OS (distutils). Flask 3 needs a newer one,
# but pip refuses to uninstall distutils-managed packages. The flag tells
# pip to install the new version on top (it shadows the old one).
COPY requirements.txt /tmp/requirements.txt

# Hard pins that nothing downstream is allowed to move. We use the base
# version (no +cu124 suffix) — pip matches 2.4.1 against the installed
# 2.4.1+cu124 fine, and this avoids local-version matching quirks.
RUN printf '%s\n' \
        'torch==2.4.1' \
        'torchvision==0.19.1' \
        'numpy==1.26.4' \
        > /tmp/constraints.txt

# The install sequence below is ordered deliberately:
#   1. Purge every numpy the base image shipped (may be >1, via OS + pip).
#   2. Install pinned numpy 1.x FIRST — torch 2.4.1 was compiled against
#      numpy 1.x and breaks at runtime under numpy 2.x (the
#      '_signature_descriptor' error that also poisons CUDA init).
#   3. Install the CUDA build of torch from the PyTorch index.
#   4. Install everything else UNDER the constraint file so nothing —
#      including transitive deps — is allowed to move numpy or torch.
#   5. Force numpy back to 1.26.4 cleanly in case step 4 slipped a 2.x in.
#   6. Verify: the build FAILS here if torch, numpy, or the numpy<->torch
#      bridge is wrong, so a broken image can never reach a student.
RUN pip install --upgrade pip \
    && (pip uninstall -y numpy 2>/dev/null || true) \
    && (pip uninstall -y numpy 2>/dev/null || true) \
    && pip install "numpy==1.26.4" \
    && pip install --index-url https://download.pytorch.org/whl/cu124 \
        torch==2.4.1 torchvision==0.19.1 \
    && pip install \
        --constraint /tmp/constraints.txt \
        --extra-index-url https://download.pytorch.org/whl/cu124 \
        --ignore-installed blinker \
        -r /tmp/requirements.txt \
    && pip install --force-reinstall --no-deps "numpy==1.26.4" \
    && python -c "import numpy as np; import torch; import clip; \
assert np.__version__.startswith('1.26'), 'numpy is '+np.__version__; \
assert torch.__version__.startswith('2.4.1'), 'torch is '+torch.__version__; \
x = torch.from_numpy(np.zeros(3, dtype=np.float32)); \
print('Build pins OK - torch', torch.__version__, '| numpy', np.__version__, '| clip OK | bridge works')"

# Copy the rest of the module content. Note: when running via docker-compose,
# the labs/ folder is bind-mounted over this, so student edits persist on the host.
COPY --chown=${USERNAME}:${USERNAME} . /workspace

RUN chmod +x /workspace/docker-entrypoint.sh

USER ${USERNAME}

# Default ports
#   8000 — launcher (Flask)
#   8888 — JupyterLab
EXPOSE 8000 8888

ENTRYPOINT ["/workspace/docker-entrypoint.sh"]
