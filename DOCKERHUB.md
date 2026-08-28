# Deep Learning Concepts and Techniques (Computer Vision)

A 15-lab, self-contained computer vision course container — perceptrons through diffusion models. Pull it, run it, open one URL, and every lab is ready to go in JupyterLab.

Source: https://github.com/traptracker-ai/deep-learning-cv

---

## Quick start

```bash
mkdir deep-learning-cv && cd deep-learning-cv
mkdir labs

docker run -d \
  --name deep-learning-cv \
  -p 7144:7144 -p 7154:7154 \
  -v "$(pwd)/labs:/workspace/labs" \
  -e JUPYTER_TOKEN=deep-learning-cv \
  --gpus all \
  --shm-size=2gb \
  traptracker-ai/deep-learning-cv:latest
```

Then open **http://localhost:7144** — that's the lab launcher.

- `mkdir labs` first, even empty — the container detects an empty mount and seeds it with all 15 labs (notebooks, data, assets) automatically on first start. Your edits then persist on the host, and a container restart never overwrites existing work.
- No NVIDIA GPU? Drop the `--gpus all` flag. Labs 1–6 run fine on CPU; labs 7 onward (object detection training, segmentation, diffusion, etc.) need CUDA.
- To go straight to JupyterLab instead of the launcher: **http://localhost:7154/lab?token=deep-learning-cv**

### Or with docker-compose

```yaml
services:
  module:
    image: traptracker-ai/deep-learning-cv:latest
    container_name: deep-learning-cv
    ports:
      - "7144:7144"
      - "7154:7154"
    volumes:
      - ./labs:/workspace/labs
    environment:
      - JUPYTER_TOKEN=deep-learning-cv
    gpus: all
    shm_size: '2gb'
```

Save as `docker-compose.yml` next to an empty `labs/` folder, then `docker compose up -d`.

---

## What's inside

| # | Lab |
|---|-----|
| 1 | Perceptrons and Multi-Layer Perceptrons |
| 2 | Your first PyTorch model — binary classification |
| 3 | Convolutional Neural Networks for image classification |
| 4 | CIFAR-10, overfitting, and data augmentation |
| 5 | Deep learning with custom image data |
| 6 | Annotating images for object detection |
| 7 | Training a YOLO26 object detector |
| 8 | Honest evaluation of an object detector |
| 9 | Zero-shot detection and the build-vs-prompt decision |
| 10 | Instance segmentation: from boxes to masks |
| 11 | Explainability: Grad-CAM and saliency maps |
| 12 | Vision Transformers: attention instead of convolution |
| 13 | Inside CLIP: contrastive learning and multi-modal retrieval |
| 14 | Generative models: autoencoders and GANs |
| 15 | Diffusion models: from noise to photorealistic images |

Every lab is a self-contained Jupyter notebook with learning outcomes, worked explanations, hands-on exercises, and reflection questions.

## GPU requirements

Built on a CUDA 12.8 base image. Labs 7, 9, 10, and 15 in particular load real models (YOLO26, SAM, Stable Diffusion) into GPU memory — a card with **24GB VRAM** (RTX 3090/4090 class or better) comfortably fits every lab. Working through several labs in one sitting? Shut down a lab's Jupyter kernel (Kernel → Shut Down Kernel) before starting the next one — JupyterLab keeps kernels running in the background otherwise, and their GPU memory adds up.

## Lab 6's image pool

Lab 6 (image annotation) expects a folder of unlabelled wildlife photos in `labs/lab06_image_annotation/data/images/` — not bundled in this image (size/licensing). See that folder's `README.md` inside the container for details once you're set up; your instructor provides this pool separately.

## License

© 2026 Paul Fergus. Free for student and research use — commercial use is strictly prohibited. See the `LICENSE` file in the source repo for the full terms.
