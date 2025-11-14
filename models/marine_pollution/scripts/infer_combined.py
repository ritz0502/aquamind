# import cv2, torch, numpy as np
# from torchvision import models, transforms
# from PIL import Image
# from scripts.train_unet import UNet

# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# # Load models
# unet = UNet().to(DEVICE)
# unet.load_state_dict(torch.load("checkpoints/unet_best.pth", map_location=DEVICE))
# unet.eval()

# resnet = models.resnet50()
# resnet.fc = torch.nn.Linear(resnet.fc.in_features, 3)
# resnet.load_state_dict(torch.load("checkpoints/resnet50_best.pth", map_location=DEVICE))
# resnet.to(DEVICE).eval()

# classes = ["plastic", "paper", "trash"]

# transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor()
# ])

# def segment(img):
#     h, w, _ = img.shape
#     inp = cv2.resize(img, (256, 256)) / 255.0
#     tensor = torch.tensor(inp.transpose(2,0,1)).unsqueeze(0).float().to(DEVICE)
#     with torch.no_grad():
#         pred = unet(tensor)[0,0].cpu().numpy()
#     mask = (pred > 0.5).astype(np.uint8) * 255
#     return cv2.resize(mask, (w, h))

# def classify(crop):
#     pil_img = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
#     tensor = transform(pil_img).unsqueeze(0).to(DEVICE)
#     with torch.no_grad():
#         pred = torch.argmax(resnet(tensor)).item()
#     return classes[pred]

# def visualize(img, mask, label):
#     overlay = img.copy()
#     overlay[mask > 0] = (0.3 * overlay[mask > 0] + 0.7 * np.array([0, 0, 255])).astype(np.uint8)
#     vis = cv2.addWeighted(img, 0.6, overlay, 0.4, 0)
#     cv2.putText(vis, f"Pollution: {label}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 
#                 1, (255, 255, 255), 3, cv2.LINE_AA)
#     return vis

# def infer_combined(img_path):
#     img = cv2.imread(img_path)
#     mask = segment(img)
#     y, x = np.where(mask > 0)
#     if len(y) == 0:
#         print("✅ No pollution detected.")
#         return
#     x1, x2, y1, y2 = np.min(x), np.max(x), np.min(y), np.max(y)
#     crop = img[y1:y2, x1:x2]
#     label = classify(crop)
#     vis = visualize(img, mask, label)
#     cv2.imwrite("outputs/final_overlay.jpg", vis)
#     print(f"✅ Detected {label} pollution. Output saved to outputs/final_overlay.jpg")

# if __name__ == "__main__":
#     infer_combined("data/test_images/ocean_pollution1.jpg")




# """
# scripts/7_infer_combined.py
# ----------------------------------------------------
# 🧠 Combines:
#  - U-Net segmentation (from train_unet.py)
#  - Pollution type classification (trained on ResNet50 embeddings)
#  - LLM-based text explanation
#  - Final visualization overlay and JSON output

# ✅ Fully consistent with 2048-D feature classifier
# ✅ Supports CPU/GPU
# ✅ Creates mask, overlay, and explanation
# ----------------------------------------------------
# """

# import os
# import sys
# import json
# import cv2
# import torch
# import numpy as np
# import joblib
# from transformers import pipeline
# from torchvision import models, transforms
# import torch.nn as nn

# # -----------------------------------------------------
# # SETUP & IMPORTS
# # -----------------------------------------------------
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# from train_unet import UNet  # ensure file is renamed (scripts/train_unet.py)

# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# CHECKPOINT_DIR = "checkpoints"
# OUTPUT_DIR = "outputs"
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # -----------------------------------------------------
# # LOAD MODELS
# # -----------------------------------------------------
# print("🚀 Loading models...")

# # 1️⃣ Load U-Net
# unet = UNet().to(DEVICE)
# unet.load_state_dict(torch.load(os.path.join(CHECKPOINT_DIR, "unet_best.pth"), map_location=DEVICE))
# unet.eval()

# # 2️⃣ Load RandomForest classifier and label map
# clf = joblib.load(os.path.join(CHECKPOINT_DIR, "pollution_type_classifier.pkl"))
# label_map = joblib.load(os.path.join(CHECKPOINT_DIR, "label_map.pkl"))

# # 3️⃣ Load ResNet50 feature extractor (same used during training)
# resnet = models.resnet50(weights="IMAGENET1K_V2")
# resnet.fc = nn.Identity()  # remove classification head to get 2048-D features
# resnet = resnet.to(DEVICE).eval()

# # 4️⃣ Load text generator (LLM)
# gen = pipeline("text-generation", model="distilgpt2", device=0 if DEVICE == "cuda" else -1)

# print("✅ All models loaded successfully.\n")


# # -----------------------------------------------------
# # IMAGE TRANSFORM (for ResNet feature extraction)
# # -----------------------------------------------------
# img_transform = transforms.Compose([
#     transforms.ToPILImage(),
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406],
#                          std=[0.229, 0.224, 0.225])
# ])


# # -----------------------------------------------------
# # SEGMENTATION FUNCTION
# # -----------------------------------------------------
# def segment_image(img):
#     """Generate binary mask using U-Net."""
#     h, w, _ = img.shape
#     inp = cv2.resize(img, (256, 256)) / 255.0
#     tensor = torch.tensor(inp.transpose(2, 0, 1)).unsqueeze(0).float().to(DEVICE)

#     with torch.no_grad():
#         pred = unet(tensor)[0, 0].cpu().numpy()

#     mask = (pred > 0.5).astype(np.uint8) * 255
#     return cv2.resize(mask, (w, h))


# # -----------------------------------------------------
# # FEATURE EXTRACTION (ResNet 2048D)
# # -----------------------------------------------------
# def extract_features(img, mask):
#     """Extract 2048-D ResNet features from masked region."""
#     # Apply mask to focus on polluted region
#     masked = cv2.bitwise_and(img, img, mask=mask)
#     tensor = img_transform(masked).unsqueeze(0).to(DEVICE)
#     with torch.no_grad():
#         features = resnet(tensor).cpu().numpy().flatten()
#     return features


# # -----------------------------------------------------
# # VISUALIZATION OVERLAY
# # -----------------------------------------------------
# def overlay_mask(img, mask, label):
#     """Overlay segmentation mask + label text."""
#     overlay = img.copy()
#     overlay[mask > 0] = (0.3 * overlay[mask > 0] + 0.7 * np.array([0, 0, 255])).astype(np.uint8)
#     vis = cv2.addWeighted(img, 0.6, overlay, 0.4, 0)
#     cv2.putText(vis, f"Detected: {label}", (20, 40),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3, cv2.LINE_AA)
#     return vis


# # -----------------------------------------------------
# # MAIN INFERENCE PIPELINE
# # -----------------------------------------------------
# def predict(image_path):
#     img = cv2.imread(image_path)
#     if img is None:
#         raise FileNotFoundError(f"❌ Image not found: {image_path}")

#     # 1️⃣ Run segmentation
#     mask = segment_image(img)
#     cv2.imwrite(os.path.join(OUTPUT_DIR, "mask.png"), mask)

#     # 2️⃣ Check if pollution region exists
#     ys, xs = np.where(mask > 0)
#     if len(xs) == 0:
#         print("✅ No pollution detected in this image.")
#         return {
#             "type": "none",
#             "explanation": "No visible pollution detected — environment appears clean."
#         }

#     # 3️⃣ Crop polluted region
#     x1, x2, y1, y2 = np.min(xs), np.max(xs), np.min(ys), np.max(ys)
#     crop = img[y1:y2, x1:x2]
#     crop_mask = mask[y1:y2, x1:x2]

#     # 4️⃣ Extract features & classify
#     feats = extract_features(crop, crop_mask).reshape(1, -1)
#     pred = clf.predict(feats)[0]
#     pollution_type = label_map.get(pred, "unknown")

#     # 5️⃣ Generate LLM explanation
#     text = f"The detected pollution type is {pollution_type}. Suggest one short cleanup action."
#     explanation = gen(text, max_new_tokens=60, do_sample=False)[0]["generated_text"]

#     # 6️⃣ Create annotated visualization
#     vis = overlay_mask(img, mask, pollution_type)
#     vis_path = os.path.join(OUTPUT_DIR, "final_result.jpg")
#     cv2.imwrite(vis_path, vis)

#     # 7️⃣ Save structured result
#     result = {
#         "image": image_path,
#         "mask_path": os.path.join(OUTPUT_DIR, "mask.png"),
#         "annotated_path": vis_path,
#         "type": pollution_type,
#         "explanation": explanation
#     }

#     with open(os.path.join(OUTPUT_DIR, "result.json"), "w", encoding="utf-8") as f:
#         json.dump(result, f, indent=2)

#     print(f"\n✅ Pollution type: {pollution_type}")
#     print(f"💬 Explanation: {explanation}")
#     print(f"🖼️ Results saved in {OUTPUT_DIR}/\n")

#     return result


# # -----------------------------------------------------
# # ENTRY POINT
# # -----------------------------------------------------
# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python scripts/7_infer_combined.py <image_path>")
#         sys.exit(1)
#     predict(sys.argv[1])



































# """
# scripts/7_infer_combined_fast_fixed.py
# ----------------------------------------------------
# ⚡ Fast + Accurate Marine Pollution Detection
# ✅ Fixes false positives (like transparent plastic misread as glass)
# ✅ Uses largest contour for clean segmentation
# ✅ Adds heuristic bias for transparency + color
# ✅ No LLM — instant rule-based explanations
# ✅ Fully CPU-optimized
# ----------------------------------------------------
# """

# import os
# import sys
# import json
# import cv2
# import torch
# import numpy as np
# import joblib
# import torch.nn as nn
# from torchvision import models, transforms

# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# from train_unet import UNet 
# # from train_unet import UNet  # change to 5_train_unet if needed

# # ====================================================
# # SETUP
# # ====================================================
# torch.set_num_threads(4)
# os.environ["OMP_NUM_THREADS"] = "4"

# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# CHECKPOINT_DIR = "checkpoints"
# OUTPUT_DIR = "outputs"
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # ====================================================
# # LOAD MODELS
# # ====================================================
# print("🚀 Loading models (optimized)...")

# # U-Net for segmentation
# unet = UNet().to(DEVICE)
# unet.load_state_dict(torch.load(os.path.join(CHECKPOINT_DIR, "unet_best.pth"), map_location=DEVICE))
# unet.eval()

# # MobileNet for features
# from torchvision.models import mobilenet_v3_small, MobileNet_V3_Small_Weights
# mobilenet = mobilenet_v3_small(weights=MobileNet_V3_Small_Weights.DEFAULT)
# mobilenet.classifier = nn.Identity()  # remove final head
# mobilenet.to(DEVICE).eval()

# # Classifier and labels
# clf = joblib.load(os.path.join(CHECKPOINT_DIR, "pollution_type_classifier.pkl"))
# label_map = joblib.load(os.path.join(CHECKPOINT_DIR, "label_map.pkl"))

# print("✅ All models loaded successfully.\n")

# # ====================================================
# # IMAGE TRANSFORM
# # ====================================================
# transform = transforms.Compose([
#     transforms.ToPILImage(),
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406],
#                          std=[0.229, 0.224, 0.225])
# ])

# # ====================================================
# # SEGMENTATION UTILS
# # ====================================================
# def segment_main_object(img):
#     """Get clean mask of largest pollution region."""
#     h, w, _ = img.shape
#     inp = cv2.resize(img, (128, 128)) / 255.0
#     tensor = torch.tensor(inp.transpose(2, 0, 1)).unsqueeze(0).float().to(DEVICE)

#     with torch.no_grad():
#         pred = unet(tensor)[0, 0].cpu().numpy()
#     mask = (pred > 0.5).astype(np.uint8) * 255
#     mask = cv2.resize(mask, (w, h))

#     # Morphological cleanup
#     mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
#     mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

#     # Largest contour only
#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     if not contours:
#         return np.zeros_like(mask)
#     largest = max(contours, key=cv2.contourArea)
#     mask_clean = np.zeros_like(mask)
#     cv2.drawContours(mask_clean, [largest], -1, 255, -1)
#     return mask_clean

# # ====================================================
# # FEATURE EXTRACTION
# # ====================================================
# def extract_features(crop):
#     """Extract 512-D features from MobileNet."""
#     tensor = transform(crop).unsqueeze(0).to(DEVICE)
#     with torch.no_grad():
#         feats = mobilenet(tensor).cpu().numpy().flatten()
#     return feats

# # ====================================================
# # COLOR HEURISTICS
# # ====================================================
# def heuristic_adjustment(label, crop, mask):
#     hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
#     mean_v = hsv[:, :, 2].mean()
#     mean_s = hsv[:, :, 1].mean()
#     area_ratio = mask.sum() / (mask.shape[0] * mask.shape[1] + 1e-5)

#     # Bias for transparent (plastic)
#     if mean_v > 150 and mean_s < 60:
#         label = "plastic"

#     # Bias if underwater (bluish dominant)
#     mean_b = crop[:, :, 0].mean()
#     mean_g = crop[:, :, 1].mean()
#     mean_r = crop[:, :, 2].mean()
#     if mean_b > mean_r + 15 and mean_b > mean_g + 10:
#         label = "plastic"

#     # Bias if small thin shape — likely not trash
#     if area_ratio < 0.05:
#         label = "plastic"

#     return label

# # ====================================================
# # EXPLANATION GENERATOR (FAST RULE-BASED)
# # ====================================================
# ACTIONS = {
#     "plastic": "Collect floating plastic debris and recycle properly.",
#     "paper": "Remove and dispose paper waste responsibly.",
#     "trash": "Gather visible litter for safe disposal.",
#     "metal": "Retrieve metallic waste and send for recycling.",
#     "glass": "Handle glass carefully and dispose at collection points.",
#     "cardboard": "Dry and recycle cardboard material safely."
# }

# # ====================================================
# # VISUALIZATION
# # ====================================================
# def visualize(img, mask, label):
#     overlay = img.copy()
#     overlay[mask > 0] = (0.3 * overlay[mask > 0] + 0.7 * np.array([0, 0, 255])).astype(np.uint8)
#     vis = cv2.addWeighted(img, 0.6, overlay, 0.4, 0)
#     cv2.putText(vis, f"Detected: {label}", (20, 40),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
#     return vis

# # ====================================================
# # MAIN INFERENCE
# # ====================================================
# def predict(image_path):
#     img = cv2.imread(image_path)
#     if img is None:
#         raise FileNotFoundError(f"Image not found: {image_path}")

#     print(f"🔍 Processing: {image_path}")
#     mask = segment_main_object(img)
#     cv2.imwrite(os.path.join(OUTPUT_DIR, "mask.png"), mask)

#     # Find pollution region
#     ys, xs = np.where(mask > 0)
#     if len(xs) == 0:
#         print("✅ No pollution detected.")
#         return {"type": "none", "explanation": "Clean water — no visible debris."}

#     x1, x2, y1, y2 = np.min(xs), np.max(xs), np.min(ys), np.max(ys)
#     crop = img[y1:y2, x1:x2]
#     crop_mask = mask[y1:y2, x1:x2]

#     feats = extract_features(crop).reshape(1, -1)
#     pred = clf.predict(feats)[0]
#     label = label_map.get(pred, "unknown")

#     # Apply color/shape bias fix
#     label = heuristic_adjustment(label, crop, crop_mask)
#     explanation = ACTIONS.get(label, "Clean environment detected.")

#     vis = visualize(img, mask, label)
#     vis_path = os.path.join(OUTPUT_DIR, "final_overlay.jpg")
#     cv2.imwrite(vis_path, vis)

#     result = {
#         "image": image_path,
#         "mask_path": os.path.join(OUTPUT_DIR, "mask.png"),
#         "annotated_path": vis_path,
#         "type": label,
#         "explanation": explanation
#     }

#     with open(os.path.join(OUTPUT_DIR, "result.json"), "w", encoding="utf-8") as f:
#         json.dump(result, f, indent=2)

#     print(f"\n✅ Detected: {label}")
#     print(f"💬 {explanation}")
#     print(f"🖼️ Results saved in {OUTPUT_DIR}/")
#     return result

# # ====================================================
# # ENTRY POINT
# # ====================================================
# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python scripts/7_infer_combined_fast_fixed.py <image_path>")
#         sys.exit(1)
#     predict(sys.argv[1])



































# scripts/7_infer_combined_efficientnet.py
"""
Final Combined Inference Script
--------------------------------
✅ Uses U-Net (segmentation) + EfficientNet (classification)
✅ Automatically identifies pollution type
✅ Produces mask + annotated image + explanation
"""

import os, sys, json, cv2, torch, joblib
import numpy as np
from torchvision import transforms, models
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights

# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from marine_pollution.scripts.train_unet import UNet
  # or 5_train_unet if needed

# ====================================================
# CONFIG
# ====================================================
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # scripts/
ROOT_DIR = os.path.dirname(BASE_DIR)                    # marine_pollution/

CHECKPOINT_DIR = os.path.join(ROOT_DIR, "checkpoints")
OUTPUT_DIR = os.path.join(ROOT_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("🚀 Loading models...")

# U-Net for segmentation
unet = UNet().to(DEVICE)
unet.load_state_dict(torch.load(os.path.join(CHECKPOINT_DIR, "unet_best.pth"), map_location=DEVICE))
unet.eval()

# EfficientNet for embeddings
effnet = efficientnet_b0(weights=EfficientNet_B0_Weights.DEFAULT)
effnet.classifier = torch.nn.Identity()
effnet.to(DEVICE).eval()

# RandomForest Classifier
clf = joblib.load(os.path.join(CHECKPOINT_DIR, "pollution_type_classifier_finetuned.pkl"))
label_map = joblib.load(os.path.join(CHECKPOINT_DIR, "label_map.pkl"))

print("✅ Models loaded successfully.")

transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# ====================================================
# FUNCTIONS
# ====================================================
def segment(img):
    """Get main pollution mask"""
    h, w, _ = img.shape
    inp = cv2.resize(img, (128, 128)) / 255.0
    tensor = torch.tensor(inp.transpose(2, 0, 1)).unsqueeze(0).float().to(DEVICE)
    with torch.no_grad():
        pred = unet(tensor)[0, 0].cpu().numpy()
    mask = (pred > 0.5).astype(np.uint8) * 255
    mask = cv2.resize(mask, (w, h))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        mask = np.zeros_like(mask)
        cv2.drawContours(mask, [max(contours, key=cv2.contourArea)], -1, 255, -1)
    return mask

def extract_features(crop):
    tensor = transform(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        feats = effnet(tensor).cpu().numpy().flatten()
    return feats

# def predict(image_path):
#     img = cv2.imread(image_path)
#     if img is None:
#         raise FileNotFoundError(f"Image not found: {image_path}")

#     mask = segment(img)
#     ys, xs = np.where(mask > 0)
#     if len(xs) == 0:
#         print("✅ No pollution detected.")
#         return

#     x1, x2, y1, y2 = np.min(xs), np.max(xs), np.min(ys), np.max(ys)
#     crop = img[y1:y2, x1:x2]
#     feats = extract_features(crop).reshape(1, -1)
#     pred = clf.predict(feats)[0]
#     label = label_map.get(pred, "unknown")

#     explanation = {
#         "plastic": "Detected floating plastic debris — recommended cleanup and recycling.",
#         "paper": "Paper waste detected — biodegradable, but remove to maintain water clarity.",
#         "glass": "Glass item detected — remove carefully to prevent harm to marine life.",
#         "metal": "Metal object found — retrieve safely and recycle.",
#         "cardboard": "Cardboard detected — likely floating packaging waste.",
#         "trash": "Mixed trash detected — initiate cleanup."
#     }.get(label, "Clean water — no visible pollution.")

#     overlay = img.copy()
#     overlay[mask > 0] = (0.4 * overlay[mask > 0] + 0.6 * np.array([0, 0, 255])).astype(np.uint8)
#     vis = cv2.addWeighted(img, 0.6, overlay, 0.4, 0)
#     cv2.putText(vis, f"Detected: {label}", (20, 40),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

#     cv2.imwrite(os.path.join(OUTPUT_DIR, "mask.png"), mask)
#     cv2.imwrite(os.path.join(OUTPUT_DIR, "final_overlay.jpg"), vis)
#     result = {
#         "image": image_path,
#         "type": label,
#         "explanation": explanation,
#         "mask": "outputs/mask.png",
#         "annotated": "outputs/final_overlay.jpg"
#     }

#     with open(os.path.join(OUTPUT_DIR, "result.json"), "w") as f:
#         json.dump(result, f, indent=2)

#     print(f"\n✅ Detected: {label}")
#     print(f"💬 {explanation}")
#     print("🖼️ Results saved in outputs/")



def predict(input_source):
    """
    Run pollution detection on either:
    - a local file path (string)
    - or a file object (like Flask upload)
    """
    # Handle both file path and uploaded file
    if isinstance(input_source, str):
        img = cv2.imread(input_source)
        if img is None:
            raise FileNotFoundError(f"Image not found: {input_source}")
    else:
        # Read file bytes from upload
        file_bytes = np.frombuffer(input_source.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    mask = segment(img)
    ys, xs = np.where(mask > 0)
    if len(xs) == 0:
        return {
            "type": "none",
            "explanation": "No visible pollution detected.",
            "mask": None,
            "annotated": None
        }

    x1, x2, y1, y2 = np.min(xs), np.max(xs), np.min(ys), np.max(ys)
    crop = img[y1:y2, x1:x2]
    feats = extract_features(crop).reshape(1, -1)
    pred = clf.predict(feats)[0]
    label = label_map.get(pred, "unknown")

    explanation = {
        "plastic": "Detected floating plastic debris — recommended cleanup and recycling.",
        "paper": "Paper waste detected — biodegradable, but remove to maintain water clarity.",
        "glass": "Glass item detected — remove carefully to prevent harm to marine life.",
        "metal": "Metal object found — retrieve safely and recycle.",
        "cardboard": "Cardboard detected — likely floating packaging waste.",
        "trash": "Mixed trash detected — initiate cleanup."
    }.get(label, "Clean water — no visible pollution.")

    overlay = img.copy()
    overlay[mask > 0] = (0.4 * overlay[mask > 0] + 0.6 * np.array([0, 0, 255])).astype(np.uint8)
    vis = cv2.addWeighted(img, 0.6, overlay, 0.4, 0)
    cv2.putText(vis, f"Detected: {label}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    mask_path = os.path.join(OUTPUT_DIR, "mask.png")
    overlay_path = os.path.join(OUTPUT_DIR, "final_overlay.jpg")

    cv2.imwrite(mask_path, mask)
    cv2.imwrite(overlay_path, vis)

    result = {
        "type": label,
        "explanation": explanation,
        "mask": mask_path,
        "annotated": overlay_path
    }

    return result

# ====================================================
# ENTRY POINT
# ====================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/7_infer_combined_efficientnet.py <image_path>")
        sys.exit(1)
    predict(sys.argv[1])
