# Cell images dataset

## What's here

This folder contains **4,000 synthetic cell images** (1,400 / 300 / 300 per class for train / val / test) generated to teach the image-folder loading pipeline. They are deliberately made to *look like* Giemsa-stained red blood cells with optional Plasmodium parasites, but they are not real biological samples.

```
cell_images/
├── train/
│   ├── parasitized/      (1,400 images, dark spot present)
│   └── uninfected/       (1,400 images, no spot)
├── val/
│   ├── parasitized/      (300)
│   └── uninfected/       (300)
└── test/
    ├── parasitized/      (300)
    └── uninfected/       (300)
```

Each image is 130×130 JPEG. Parasitized images have one to three small dark purple/blue spots; uninfected images are clean. The task is easy on synthetic data — a small CNN should hit very high accuracy quickly. That makes for a clean teaching example.

## Why synthetic?

The original NIH "Malaria Cell Images Dataset" is 27,558 real microscopy images and is gated behind an NIH/Kaggle download that we cannot embed in a Docker image. Synthetic images let the lab run out-of-the-box in any container with no external dependency.

## Swapping in the real NIH dataset

If you want to use the real dataset for teaching or research, download it from either:

- **NIH:** https://ceb.nlm.nih.gov/repositories/malaria-datasets/
- **Kaggle mirror:** https://www.kaggle.com/datasets/iarunava/cell-images-for-detecting-malaria

The download gives you a folder `cell_images/Parasitized/` and `cell_images/Uninfected/` (note the capital letters). To use it in this lab:

1. Delete the contents of this `cell_images/` folder.
2. Split the NIH images into a 70 / 15 / 15 train / val / test structure matching the layout above.
3. Lower-case the folder names to `parasitized/` and `uninfected/`.

A short helper script for this is included as `prepare_nih_dataset.py` next to this README.

**No code changes to the notebook are required.** The PyTorch `ImageFolder` loader will pick up whatever images live in this folder structure.
