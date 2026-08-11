# Ground-truth test set for Lab 8

This lab is **strictly real-data only** — nothing is bundled. You build the test
set yourself, which is the whole point: honest evaluation requires data the model
has never seen, sourced independently of training.

## What goes here

- `holdout_images/` — at least 30 real wildlife photographs (JPEG) that you have
  the right to use (CC-licensed from iNaturalist / Wikimedia / Flickr, or your own).
  Try to source images that differ from your Lab 6/7 training set — different
  lighting, season, camera, angle — so the generalisation gap becomes visible.

- `holdout_labels/` — one YOLO-format `.txt` per image (matching filename stem),
  produced by annotating each image in the Lab 6 annotator. These are your
  *ground truth* — the hand-verified correct answers the model is judged against.

Class order (must match Lab 6/7): `0 buffalo, 1 elephant, 2 rhino, 3 zebra`.

See Section 2 of `lab08.ipynb` for the full sourcing-and-annotating walkthrough.
