# scripts/8_generate_ocean_augmentations.py
"""
Generate Ocean-Style Augmentations
----------------------------------
✅ Simulates underwater lighting and colors
✅ Applies to all folders in data/training_dataset/
✅ Outputs to data/ocean_augmented_dataset/
"""

import os
import cv2
import numpy as np
from tqdm import tqdm

INPUT_DIR = "training_dataset/"
OUTPUT_DIR = "data/ocean_augmented_dataset"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def add_blue_tint(img):
    """Adds underwater-like blue-green hue."""
    blue = np.full_like(img, (30, 80, 150))
    return cv2.addWeighted(img, 0.7, blue, 0.3, 0)

def add_waves(img):
    """Simulates light refraction ripples."""
    h, w = img.shape[:2]
    dx = (np.random.randn(h, w) * 2).astype(np.float32)
    dy = (np.random.randn(h, w) * 2).astype(np.float32)
    mapx, mapy = np.meshgrid(np.arange(w), np.arange(h))
    mapx = (mapx + dx).astype(np.float32)
    mapy = (mapy + dy).astype(np.float32)
    return cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

def adjust_brightness_contrast(img):
    alpha = np.random.uniform(0.8, 1.3)  # contrast
    beta = np.random.uniform(-30, 30)    # brightness
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

def augment_class_folder(cls_folder, out_folder):
    os.makedirs(out_folder, exist_ok=True)
    for fname in tqdm(os.listdir(cls_folder), desc=f"🌊 {os.path.basename(cls_folder)}"):
        if not fname.lower().endswith((".jpg", ".png", ".jpeg")):
            continue
        img_path = os.path.join(cls_folder, fname)
        img = cv2.imread(img_path)
        if img is None: continue

        img = cv2.resize(img, (256, 256))
        img = add_blue_tint(img)
        img = add_waves(img)
        img = adjust_brightness_contrast(img)

        out_path = os.path.join(out_folder, fname)
        cv2.imwrite(out_path, img)

def main():
    for cls in os.listdir(INPUT_DIR):
        cls_folder = os.path.join(INPUT_DIR, cls)
        if not os.path.isdir(cls_folder): continue
        out_folder = os.path.join(OUTPUT_DIR, cls)
        augment_class_folder(cls_folder, out_folder)

if __name__ == "__main__":
    main()
