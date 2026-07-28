"""
Helper script for swapping the synthetic cell images for the real NIH dataset.

Usage:
    1. Download the NIH Malaria Cell Images Dataset (either the .zip from kaggle
       or the .zip from the NIH page).
    2. Extract it somewhere. You should have a folder structure like:
           cell_images/
             Parasitized/
               C100P61ThinF_IMG_20150918_144104_cell_162.png
               ...
             Uninfected/
               C100P61ThinF_IMG_20150918_144104_cell_169.png
               ...
    3. Run this script, passing in the path to the *parent* of those
       Parasitized/ and Uninfected/ folders:

           python prepare_nih_dataset.py /path/to/extracted/cell_images

The script will:
    - Wipe the existing data/cell_images/{train,val,test} structure.
    - Re-split the NIH images 70/15/15 into the structure this lab expects.
    - Lower-case folder names.
    - Preserve the original file names so you can trace any image back to its source.
"""
from __future__ import annotations

import argparse
import random
import shutil
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
OUT = THIS_DIR / "cell_images"

SEED = 7144
SPLIT_RATIOS = (0.70, 0.15, 0.15)   # train, val, test


def main() -> None:
    parser = argparse.ArgumentParser(description="Re-split NIH cell images into train/val/test.")
    parser.add_argument("source", type=Path,
                        help="Path to the folder containing Parasitized/ and Uninfected/")
    args = parser.parse_args()

    source = args.source
    para_src = source / "Parasitized"
    unin_src = source / "Uninfected"
    if not para_src.is_dir() or not unin_src.is_dir():
        raise SystemExit(f"Expected {para_src} and {unin_src} to exist. Check the path.")

    rng = random.Random(SEED)

    # Clear the existing structure.
    for split in ("train", "val", "test"):
        for cls in ("parasitized", "uninfected"):
            target = OUT / split / cls
            if target.exists():
                shutil.rmtree(target)
            target.mkdir(parents=True, exist_ok=True)

    for class_src, class_name in [(para_src, "parasitized"), (unin_src, "uninfected")]:
        # Collect all valid image files (PNGs in the original dataset; accept JPGs too)
        files = [p for p in class_src.iterdir()
                 if p.suffix.lower() in (".png", ".jpg", ".jpeg")]
        rng.shuffle(files)

        n = len(files)
        n_train = int(n * SPLIT_RATIOS[0])
        n_val = int(n * SPLIT_RATIOS[1])

        splits = {
            "train": files[:n_train],
            "val": files[n_train:n_train + n_val],
            "test": files[n_train + n_val:],
        }

        for split_name, split_files in splits.items():
            dest = OUT / split_name / class_name
            for f in split_files:
                shutil.copy2(f, dest / f.name)
            print(f"  {class_name}/{split_name}: {len(split_files)} files -> {dest}")

    print(f"\nDone. New structure under {OUT}")


if __name__ == "__main__":
    main()
