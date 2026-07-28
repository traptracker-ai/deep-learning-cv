"""
Build a fallback annotated dataset for Lab 7.

Lab 7 normally uses the dataset students built in Lab 6. This script
provides a 'training wheels' fallback: a copy of the Lab 6 starter
images with pre-made annotations, split into train/val/test, with
a working data.yaml. The student can run Lab 7 without having
completed Lab 6.

Run from inside the container or from the host:

    python labs/lab07_yolo_training/data/build_fallback_dataset.py

The dataset is written into:

    labs/lab07_yolo_training/data/fallback_dataset/
        images/{train,val,test}/
        labels/{train,val,test}/
        data.yaml
"""
from __future__ import annotations

import random
import shutil
import yaml
from pathlib import Path

# ----- Configuration -----
HERE = Path(__file__).resolve().parent
LAB6_IMAGES = HERE.parent.parent / "lab06_image_annotation" / "data" / "images"
OUT_ROOT = HERE / "fallback_dataset"

CLASSES = ["badger", "fox", "deer", "hedgehog", "squirrel"]
CLASS_IDX = {name: i for i, name in enumerate(CLASSES)}

# Pre-made annotations (same as the test annotations we used during Lab 6 verification).
# Format: {image_stem: [(class_name, cx, cy, w, h), ...]}
ANNOTATIONS = {
    "badger_01":   [("badger",   0.55, 0.75, 0.28, 0.20)],
    "fox_01":      [("fox",      0.45, 0.72, 0.27, 0.18)],
    "deer_01":     [("deer",     0.55, 0.55, 0.18, 0.30)],
    "hedgehog_01": [("hedgehog", 0.45, 0.78, 0.18, 0.18)],
    "squirrel_01": [("squirrel", 0.35, 0.62, 0.18, 0.30)],
    "fox_02":      [("fox",      0.30, 0.74, 0.20, 0.15)],
    "deer_02":     [("deer",     0.65, 0.50, 0.21, 0.36)],
    "two_foxes":   [("fox",      0.30, 0.70, 0.24, 0.16),
                    ("fox",      0.70, 0.72, 0.18, 0.13)],
    "badger_deer": [("badger",   0.30, 0.78, 0.22, 0.18),
                    ("deer",     0.70, 0.55, 0.17, 0.28)],
    "squirrel_hedgehog": [("squirrel", 0.25, 0.55, 0.14, 0.22),
                          ("hedgehog", 0.70, 0.80, 0.15, 0.16)],
    "small_fox":   [("fox",      0.55, 0.50, 0.13, 0.10)],
    "tiny_hedgehog": [("hedgehog", 0.70, 0.85, 0.10, 0.10)],
    "edge_deer":   [("deer",     0.95, 0.55, 0.10, 0.30)],
    "edge_badger": [("badger",   0.06, 0.78, 0.13, 0.18)],
    "trio":        [("squirrel", 0.20, 0.60, 0.12, 0.22),
                    ("fox",      0.55, 0.75, 0.22, 0.15),
                    ("hedgehog", 0.85, 0.85, 0.13, 0.13)],
}

SPLIT = (0.70, 0.15, 0.15)  # train, val, test
RNG_SEED = 7144


def main() -> None:
    # Verify the source images exist.
    if not LAB6_IMAGES.is_dir():
        raise SystemExit(f"Lab 6 image folder not found: {LAB6_IMAGES}")

    source_files = sorted(LAB6_IMAGES.glob("*.jpg"))
    if not source_files:
        raise SystemExit(f"No jpg images found in {LAB6_IMAGES}")
    print(f"Found {len(source_files)} source images.")

    # Build the directory layout.
    for split in ("train", "val", "test"):
        (OUT_ROOT / "images" / split).mkdir(parents=True, exist_ok=True)
        (OUT_ROOT / "labels" / split).mkdir(parents=True, exist_ok=True)

    # Filter to images we have annotations for.
    annotated = [p for p in source_files if p.stem in ANNOTATIONS]
    missing = [p for p in source_files if p.stem not in ANNOTATIONS]
    if missing:
        print(f"  (skipping {len(missing)} images with no annotations: {[m.stem for m in missing]})")

    # Deterministic split.
    rng = random.Random(RNG_SEED)
    files = list(annotated)
    rng.shuffle(files)
    n = len(files)
    n_train = int(n * SPLIT[0])
    n_val = int(n * SPLIT[1])
    splits = {
        "train": files[:n_train],
        "val":   files[n_train:n_train + n_val],
        "test":  files[n_train + n_val:],
    }

    for split_name, fps in splits.items():
        print(f"\n{split_name}: {len(fps)} images")
        for fp in fps:
            # Copy the image.
            shutil.copy2(fp, OUT_ROOT / "images" / split_name / fp.name)
            # Write the label file.
            label_path = OUT_ROOT / "labels" / split_name / f"{fp.stem}.txt"
            rows = []
            for class_name, cx, cy, w, h in ANNOTATIONS[fp.stem]:
                cls_id = CLASS_IDX[class_name]
                rows.append(f"{cls_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")
            label_path.write_text("\n".join(rows) + "\n")
            print(f"  {fp.name} ({len(rows)} box{'es' if len(rows) != 1 else ''})")

    # Write data.yaml.
    data_yaml = {
        "path": str(OUT_ROOT.resolve()),
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "names": {i: name for i, name in enumerate(CLASSES)},
    }
    yaml_path = OUT_ROOT / "data.yaml"
    with open(yaml_path, "w") as f:
        yaml.safe_dump(data_yaml, f, sort_keys=False)
    print(f"\nWrote {yaml_path}")

    total = sum(len(v) for v in splits.values())
    print(f"\nDone. {total} images across train/val/test ready for training.")


if __name__ == "__main__":
    main()
