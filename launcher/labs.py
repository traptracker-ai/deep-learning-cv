"""
Lab catalogue for the 7144COMP launcher.

Edit this file to add new labs, mark them as ready, or update descriptions.
The launcher reads it at startup.
"""

MODULE_INFO = {
    "code": "7144COMP",
    "title": "Deep Learning Concepts and Techniques",
    "tagline": "Nine hands-on labs from a perceptron in numpy to training YOLO26, honest evaluation, and zero-shot detection with foundation models.",
}

LABS = [
    {
        "number": 1,
        "title": "Perceptrons and Multi-Layer Perceptrons",
        "summary": "Build a perceptron from scratch on the Iris dataset, then a small MLP that solves XOR. Compare against scikit-learn.",
        "topics": ["perceptron", "MLP", "backpropagation", "scikit-learn"],
        "week": 1,
        "duration_min": 90,
        "notebook": "labs/lab01_perceptron_mlp/lab01.ipynb",
        "status": "ready",
    },
    {
        "number": 2,
        "title": "Your first PyTorch model — binary classification",
        "summary": "Build a neural network in PyTorch from the ground up: nn.Module subclass, DataLoader, explicit training loop, early stopping. Trained on the Breast Cancer Wisconsin dataset.",
        "topics": ["PyTorch", "nn.Module", "DataLoader", "binary classification", "early stopping"],
        "week": 2,
        "duration_min": 120,
        "notebook": "labs/lab02_pytorch_binary_classification/lab02.ipynb",
        "status": "ready",
    },
    {
        "number": 3,
        "title": "Convolutional Neural Networks for image classification",
        "summary": "Build a CNN in PyTorch to classify handwritten digits (MNIST) and clothing (Fashion-MNIST). Covers convolutions, pooling, three-way data splits, and visualising learned filters.",
        "topics": ["CNN", "Conv2d", "MaxPool2d", "BatchNorm", "MNIST", "Fashion-MNIST"],
        "week": 3,
        "duration_min": 150,
        "notebook": "labs/lab03_cnn_mnist/lab03.ipynb",
        "status": "ready",
    },
    {
        "number": 4,
        "title": "CIFAR-10, overfitting, and data augmentation",
        "summary": "Train a CNN on colour images, watch it overfit, then fix it with data augmentation. Side-by-side comparison of two training runs on the same architecture.",
        "topics": ["CIFAR-10", "overfitting", "data augmentation", "RandomCrop", "RandomHorizontalFlip"],
        "week": 4,
        "duration_min": 180,
        "notebook": "labs/lab04_cifar10_augmentation/lab04.ipynb",
        "status": "ready",
    },
    {
        "number": 5,
        "title": "Deep learning with custom image data",
        "summary": "Load images from a folder structure with ImageFolder, train a CNN on synthetic malaria cell microscopy images, and predict on individual files from disk.",
        "topics": ["ImageFolder", "custom data", "binary classification", "medical imaging", "transforms"],
        "week": 5,
        "duration_min": 180,
        "notebook": "labs/lab05_custom_image_data/lab05.ipynb",
        "status": "ready",
    },
    {
        "number": 6,
        "title": "Annotating images for object detection",
        "summary": "Annotate UK wildlife images in YOLO format using the built-in bounding-box tool. Produce a clean train/val/test dataset ready for the YOLO training lab.",
        "topics": ["object detection", "YOLO format", "annotation", "bounding boxes", "data.yaml"],
        "week": 6,
        "duration_min": 180,
        "notebook": "labs/lab06_image_annotation/lab06.ipynb",
        "status": "ready",
    },
    {
        "number": 7,
        "title": "Training a YOLO26 object detector",
        "summary": "Fine-tune a pretrained YOLO26x model on your annotated dataset using Ultralytics. Evaluate with mAP, run inference on new images, and export to ONNX. Requires a CUDA GPU.",
        "topics": ["YOLO26", "Ultralytics", "object detection", "mAP", "transfer learning", "ONNX export"],
        "week": 7,
        "duration_min": 240,
        "notebook": "labs/lab07_yolo_training/lab07.ipynb",
        "status": "ready",
    },
    {
        "number": 8,
        "title": "Honest evaluation of an object detector",
        "summary": "Build an independent ground-truth test set, then compute detection metrics from first principles: IoU matching, precision-recall curves, mAP, error analysis, and bootstrap confidence intervals. Learn why ROC doesn't apply to detection.",
        "topics": ["evaluation", "precision-recall", "mAP", "IoU", "error analysis", "confidence intervals"],
        "week": 8,
        "duration_min": 240,
        "notebook": "labs/lab08_detection_evaluation/lab08.ipynb",
        "status": "ready",
    },
    {
        "number": 9,
        "title": "Zero-shot detection and the build-vs-prompt decision",
        "summary": "Run a zero-shot open-vocabulary detector (YOLOE-26) with no training, compare it head-to-head against your trained YOLO26 using Lab 8's metrics, explore prompt engineering, and learn when to train vs prompt. The module capstone.",
        "topics": ["zero-shot", "open-vocabulary", "YOLOE", "foundation models", "prompt engineering", "auto-labelling"],
        "week": 9,
        "duration_min": 240,
        "notebook": "labs/lab09_zeroshot_detection/lab09.ipynb",
        "status": "ready",
    },
]
