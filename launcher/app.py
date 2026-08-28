"""
Deep Learning — module launcher
=========================================

A small Flask app that serves:
- The module landing page (`/`) listing every lab.
- A module-leader about page (`/about`).
- A bounding-box image annotator (`/annotator`) used in Lab 6.
- A health endpoint (`/health`).

Lab metadata lives in `labs.py` so it can be edited without touching templates.
The annotator's image and label directories live under the bind-mounted
`labs/lab06_image_annotation/data/` so all student work persists on the host.
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from urllib.parse import quote

from flask import Flask, jsonify, render_template, request, send_from_directory

from labs import LABS, MODULE_INFO

app = Flask(__name__)

# ============================================================
# Configuration
# ============================================================

LAUNCHER_DIR = Path(__file__).resolve().parent
WORKSPACE = LAUNCHER_DIR.parent
ANNOTATOR_DATA_DIR = WORKSPACE / "labs" / "lab06_image_annotation" / "data"
ANNOTATOR_IMAGES_DIR = ANNOTATOR_DATA_DIR / "images"
ANNOTATOR_LABELS_DIR = ANNOTATOR_DATA_DIR / "labels"

# Image filename validation — only allow simple alphanumeric + dot/underscore/dash.
SAFE_NAME = re.compile(r"^[A-Za-z0-9_.-]+\.(jpg|jpeg|png)$")


# ============================================================
# Helpers
# ============================================================

def jupyter_url(notebook_path: str) -> str:
    """Build a URL that opens a specific notebook in JupyterLab."""
    token = os.environ.get("JUPYTER_TOKEN", "deep-learning-cv")
    safe_path = quote(notebook_path.lstrip("/"))
    return f"http://localhost:7154/lab/tree/{safe_path}?token={token}"


def load_classes() -> list[str]:
    """Read the class list from data/classes.txt. Empty if the dataset has none yet."""
    classes_file = ANNOTATOR_DATA_DIR / "classes.txt"
    if classes_file.is_file():
        return [ln.strip() for ln in classes_file.read_text().splitlines() if ln.strip()]
    return []


def list_images() -> list[str]:
    """Return sorted list of all image filenames in the images folder."""
    if not ANNOTATOR_IMAGES_DIR.is_dir():
        return []
    return sorted(
        p.name for p in ANNOTATOR_IMAGES_DIR.iterdir()
        if SAFE_NAME.match(p.name)
    )


def label_path_for(image_name: str) -> Path:
    """Get the corresponding label .txt file for a given image."""
    stem = Path(image_name).stem
    return ANNOTATOR_LABELS_DIR / f"{stem}.txt"


def load_annotations(image_name: str) -> list[dict]:
    """Read a label file and return a list of normalised annotation dicts."""
    fp = label_path_for(image_name)
    if not fp.is_file():
        return []
    boxes = []
    for line in fp.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 5:
            continue
        try:
            cls_id = int(parts[0])
            cx, cy, w, h = [float(x) for x in parts[1:]]
        except ValueError:
            continue
        boxes.append({"class_id": cls_id, "cx": cx, "cy": cy, "w": w, "h": h})
    return boxes


# Per-image box counts for `/annotator/api/state`, built to stay fast at tens
# of thousands of images. Two things make it cheap:
#   1. ONE directory scan of labels/ (os.scandir), not a stat() per image —
#      30k individual stat calls over a Docker bind mount is seconds of wall
#      time; one scandir is milliseconds.
#   2. An in-process cache keyed on (mtime_ns, size), so a warm process only
#      re-reads and re-parses the handful of label files that actually
#      changed since the last page load. Files that are absent or empty never
#      get opened at all.
_box_count_cache: dict[str, tuple[int, int, int]] = {}


def _scan_label_stats() -> dict[str, os.stat_result]:
    """One pass over labels/: {stem: stat_result} for every .txt file."""
    out: dict[str, os.stat_result] = {}
    try:
        with os.scandir(ANNOTATOR_LABELS_DIR) as it:
            for entry in it:
                if entry.name.endswith(".txt") and entry.is_file():
                    out[entry.name[:-4]] = entry.stat()
    except FileNotFoundError:
        pass
    return out


def _count_from_stat(stem: str, st: os.stat_result | None) -> int:
    """YOLO row count for one label file, given its already-scanned stat. Cached."""
    if st is None or st.st_size == 0:
        return 0
    cached = _box_count_cache.get(stem)
    if cached is not None and cached[0] == st.st_mtime_ns and cached[1] == st.st_size:
        return cached[2]
    fp = ANNOTATOR_LABELS_DIR / f"{stem}.txt"
    n = sum(1 for ln in fp.read_text().splitlines() if len(ln.split()) == 5)
    _box_count_cache[stem] = (st.st_mtime_ns, st.st_size, n)
    return n


def save_annotations(image_name: str, boxes: list[dict]) -> None:
    """Write annotations in YOLO format. One row per box."""
    ANNOTATOR_LABELS_DIR.mkdir(parents=True, exist_ok=True)
    fp = label_path_for(image_name)
    lines = []
    for b in boxes:
        cx = max(0.0, min(1.0, float(b["cx"])))
        cy = max(0.0, min(1.0, float(b["cy"])))
        w = max(0.0, min(1.0, float(b["w"])))
        h = max(0.0, min(1.0, float(b["h"])))
        cls_id = int(b["class_id"])
        lines.append(f"{cls_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")
    fp.write_text("\n".join(lines) + ("\n" if lines else ""))


# ============================================================
# Routes — main launcher
# ============================================================

@app.route("/")
def index():
    labs_with_links = []
    for lab in LABS:
        labs_with_links.append({
            **lab,
            "url": jupyter_url(lab["notebook"]) if lab.get("notebook") else None,
        })
    return render_template(
        "index.html",
        module=MODULE_INFO,
        labs=labs_with_links,
    )


@app.route("/about")
def about():
    return render_template("about.html", module=MODULE_INFO)


@app.route("/health")
def health():
    return {"status": "ok"}, 200


# ============================================================
# Routes — annotator (Lab 6)
# ============================================================

@app.route("/annotator")
def annotator():
    """The single-page bounding box annotator."""
    return render_template("annotator.html", module=MODULE_INFO)


@app.route("/annotator/api/state")
def annotator_state():
    """Return the list of images, their annotation counts, and the class list."""
    images = list_images()
    stats = _scan_label_stats()
    info = []
    for name in images:
        stem = name.rsplit(".", 1)[0]
        info.append({"name": name, "n_boxes": _count_from_stat(stem, stats.get(stem))})
    return jsonify({
        "classes": load_classes(),
        "images": info,
    })


@app.route("/annotator/api/image/<path:filename>")
def annotator_image(filename):
    """Serve an image file from the annotator's images directory."""
    return send_from_directory(ANNOTATOR_IMAGES_DIR, filename)


@app.route("/annotator/api/annotations/<image_name>", methods=["GET"])
def annotator_get_annotations(image_name):
    """Return the current annotations for one image."""
    if not SAFE_NAME.match(image_name):
        return jsonify({"error": "invalid image name"}), 400
    if not (ANNOTATOR_IMAGES_DIR / image_name).is_file():
        return jsonify({"error": "image not found"}), 404
    return jsonify({
        "image": image_name,
        "boxes": load_annotations(image_name),
    })


@app.route("/annotator/api/annotations/<image_name>", methods=["POST"])
def annotator_save_annotations(image_name):
    """Save annotations for one image. Body: {boxes: [{class_id, cx, cy, w, h}, ...]}"""
    if not SAFE_NAME.match(image_name):
        return jsonify({"error": "invalid image name"}), 400
    if not (ANNOTATOR_IMAGES_DIR / image_name).is_file():
        return jsonify({"error": "image not found"}), 404

    payload = request.get_json(silent=True) or {}
    boxes = payload.get("boxes", [])
    if not isinstance(boxes, list):
        return jsonify({"error": "boxes must be a list"}), 400

    for b in boxes:
        if not isinstance(b, dict):
            return jsonify({"error": "each box must be an object"}), 400
        required = {"class_id", "cx", "cy", "w", "h"}
        if not required.issubset(b):
            return jsonify({"error": f"box missing fields: required {sorted(required)}"}), 400

    save_annotations(image_name, boxes)
    return jsonify({"status": "ok", "n_boxes": len(boxes)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7144, debug=False)
