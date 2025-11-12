# import os, torch, torch.nn as nn
# from torchvision import models, transforms, datasets
# from torch.utils.data import DataLoader
# from tqdm import tqdm

# DATA_DIR = "training_dataset"
# CHECKPOINT_DIR = "checkpoints"
# os.makedirs(CHECKPOINT_DIR, exist_ok=True)

# device = "cuda" if torch.cuda.is_available() else "cpu"

# transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.RandomHorizontalFlip(),
#     transforms.ColorJitter(0.2, 0.2, 0.2),
#     transforms.ToTensor()
# ])

# dataset = datasets.ImageFolder(DATA_DIR, transform=transform)
# train_size = int(0.8 * len(dataset))
# val_size = len(dataset) - train_size
# train_ds, val_ds = torch.utils.data.random_split(dataset, [train_size, val_size])

# train_loader = DataLoader(train_ds, batch_size=16, shuffle=True)
# val_loader = DataLoader(val_ds, batch_size=16)

# model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
# model.fc = nn.Linear(model.fc.in_features, len(dataset.classes))
# model = model.to(device)

# criterion = nn.CrossEntropyLoss()
# optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

# best_acc = 0
# for epoch in range(10):
#     model.train()
#     for imgs, labels in tqdm(train_loader, desc=f"Epoch {epoch+1}/10"):
#         imgs, labels = imgs.to(device), labels.to(device)
#         optimizer.zero_grad()
#         preds = model(imgs)
#         loss = criterion(preds, labels)
#         loss.backward()
#         optimizer.step()

#     # validation
#     model.eval(); correct=total=0
#     with torch.no_grad():
#         for imgs, labels in val_loader:
#             imgs, labels = imgs.to(device), labels.to(device)
#             _, predicted = torch.max(model(imgs), 1)
#             total += labels.size(0)
#             correct += (predicted == labels).sum().item()
#     acc = correct/total
#     print(f"Val Acc: {acc:.3f}")
#     if acc>best_acc:
#         torch.save(model.state_dict(), os.path.join(CHECKPOINT_DIR,"resnet50_best.pth"))
#         best_acc=acc
#         print("💾 Saved new best model.")







# # scripts/6_train_type_classifier.py
# import os, joblib
# import numpy as np
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report, confusion_matrix
# import matplotlib.pyplot as plt
# import seaborn as sns

# os.makedirs("checkpoints", exist_ok=True)
# X, y = joblib.load("checkpoints/features_labels.pkl")

# print(f"📊 Dataset loaded: {X.shape[0]} samples, {X.shape[1]} features")

# # Split dataset
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# # Train classifier
# clf = RandomForestClassifier(
#     n_estimators=200,
#     max_depth=10,
#     min_samples_split=3,
#     random_state=42,
#     n_jobs=-1
# )
# clf.fit(X_train, y_train)

# # Evaluate
# y_pred = clf.predict(X_test)
# print("\n📈 Classification Report:\n")
# print(classification_report(y_test, y_pred, target_names=["plastic", "paper", "trash", "metal", "glass"]))

# cm = confusion_matrix(y_test, y_pred)
# plt.figure(figsize=(5,4))
# sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["plastic", "paper", "trash", "metal", "glass"], yticklabels=["plastic", "paper", "trash", "metal", "glass"])
# plt.title("Confusion Matrix")
# plt.xlabel("Predicted")
# plt.ylabel("True")
# plt.tight_layout()
# plt.savefig("checkpoints/confusion_matrix.png")
# plt.close()

# # Save model and label map
# joblib.dump(clf, "checkpoints/pollution_type_classifier.pkl")
# joblib.dump({0: "plastic", 1: "paper", 2: "trash" , 3: "metal", 4: "glass"}, "checkpoints/label_map.pkl")
# print("\n✅ Classifier saved at checkpoints/pollution_type_classifier.pkl")
# print("🖼️ Confusion matrix saved at checkpoints/confusion_matrix.png")
































# # scripts/6_train_type_classifier.py
# import os, joblib, numpy as np, torch
# from torch import nn
# from torchvision import models, transforms
# from PIL import Image
# from tqdm import tqdm
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report, confusion_matrix
# import matplotlib.pyplot as plt
# import seaborn as sns

# # ---------------- CONFIG ----------------
# DATA_DIR = "training_dataset/"
# CHECKPOINT_DIR = "checkpoints"
# os.makedirs(CHECKPOINT_DIR, exist_ok=True)
# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# # ---------------- FEATURE EXTRACTOR ----------------
# model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
# model = nn.Sequential(*list(model.children())[:-1])  # remove classifier
# model.eval().to(DEVICE)

# transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406],
#                          std=[0.229, 0.224, 0.225])
# ])

# # ---------------- EXTRACT FEATURES ----------------
# X, y, label_map = [], [], {}
# classes = sorted(os.listdir(DATA_DIR))
# for idx, cls in enumerate(classes):
#     cls_path = os.path.join(DATA_DIR, cls)
#     if not os.path.isdir(cls_path): continue
#     label_map[idx] = cls
#     files = [f for f in os.listdir(cls_path) if f.lower().endswith(('.jpg','.png','.jpeg'))]
#     print(f"🔹 Processing {cls} ({len(files)} images)")
#     for f in tqdm(files, desc=f"{cls}"):
#         try:
#             img = Image.open(os.path.join(cls_path, f)).convert("RGB")
#             img_t = transform(img).unsqueeze(0).to(DEVICE)
#             with torch.no_grad():
#                 feat = model(img_t).squeeze().cpu().numpy()
#             X.append(feat)
#             y.append(idx)
#         except Exception as e:
#             print(f"⚠️ Skipped {f}: {e}")

# X, y = np.array(X), np.array(y)
# print(f"\n✅ Extracted feature shape: {X.shape}, Labels: {len(y)}")
# joblib.dump((X, y), os.path.join(CHECKPOINT_DIR, "deep_features.pkl"))

# # ---------------- TRAIN CLASSIFIER ----------------
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
# clf = RandomForestClassifier(n_estimators=300, max_depth=12, n_jobs=-1, random_state=42)
# clf.fit(X_train, y_train)
# y_pred = clf.predict(X_test)

# # ---------------- EVALUATE ----------------
# target_names = [label_map[i] for i in sorted(label_map.keys())]
# print("\n📈 Classification Report:\n")
# print(classification_report(y_test, y_pred, target_names=target_names))

# cm = confusion_matrix(y_test, y_pred)
# plt.figure(figsize=(6,5))
# sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=target_names, yticklabels=target_names)
# plt.title("Confusion Matrix")
# plt.xlabel("Predicted")
# plt.ylabel("True")
# plt.tight_layout()
# plt.savefig(os.path.join(CHECKPOINT_DIR, "confusion_matrix.png"))
# plt.close()

# # ---------------- SAVE MODEL ----------------
# joblib.dump(clf, os.path.join(CHECKPOINT_DIR, "pollution_type_classifier.pkl"))
# joblib.dump(label_map, os.path.join(CHECKPOINT_DIR, "label_map.pkl"))

# print(f"\n✅ Model saved in {CHECKPOINT_DIR}")

































# scripts/6_train_classifier_efficientnet.py
"""
Train Pollution Type Classifier using EfficientNet-B0 Features
---------------------------------------------------------------
✅ Uses real dataset in /data/training_dataset
✅ Extracts 1280-D embeddings from EfficientNet-B0
✅ Trains RandomForestClassifier
✅ Saves model + label map in checkpoints/
"""

import os
import cv2
import numpy as np
import joblib
import torch
from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from torchvision import transforms, models
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights

# ====================================================
# CONFIG
# ====================================================
DATA_DIR = "training_dataset/"
CHECKPOINT_DIR = "checkpoints"
os.makedirs(CHECKPOINT_DIR, exist_ok=True)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# ====================================================
# MODEL & TRANSFORMS
# ====================================================
print("🚀 Loading EfficientNet-B0 ...")
effnet = efficientnet_b0(weights=EfficientNet_B0_Weights.DEFAULT)
effnet.classifier = torch.nn.Identity()  # remove final layer
effnet.to(DEVICE).eval()

transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# ====================================================
# FEATURE EXTRACTION
# ====================================================
X, y, label_map = [], [], {}
classes = sorted([d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))])

print(f"🔹 Found classes: {classes}")

for i, cls in enumerate(classes):
    label_map[i] = cls
    folder = os.path.join(DATA_DIR, cls)
    print(f"🔹 Extracting features for {cls} ({len(os.listdir(folder))} images)")
    for fname in tqdm(os.listdir(folder)):
        if not fname.lower().endswith((".jpg", ".png", ".jpeg")):
            continue
        img_path = os.path.join(folder, fname)
        img = cv2.imread(img_path)
        if img is None:
            continue
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        tensor = transform(img_rgb).unsqueeze(0).to(DEVICE)
        with torch.no_grad():
            feat = effnet(tensor).cpu().numpy().flatten()
        X.append(feat)
        y.append(i)

X = np.array(X)
y = np.array(y)

print(f"\n✅ Extracted feature matrix: {X.shape}, labels: {len(y)}")

# ====================================================
# TRAIN CLASSIFIER
# ====================================================
print("🎯 Training RandomForestClassifier ...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

clf = RandomForestClassifier(
    n_estimators=250,
    max_depth=12,
    n_jobs=-1,
    random_state=42
)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print("\n📈 Classification Report:")
print(classification_report(y_test, y_pred, target_names=classes))

print(f"✅ Accuracy: {np.mean(y_pred == y_test):.3f}")
cm = confusion_matrix(y_test, y_pred)
print(f"🧩 Confusion Matrix:\n{cm}")

# Save
joblib.dump(clf, os.path.join(CHECKPOINT_DIR, "pollution_type_classifier.pkl"))
joblib.dump(label_map, os.path.join(CHECKPOINT_DIR, "label_map.pkl"))
print("\n💾 Saved EfficientNet classifier and label map in checkpoints/")
