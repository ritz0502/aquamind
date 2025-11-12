# scripts/8_finetune_classifier_ocean.py
"""
Fine-tune EfficientNet Classifier on Ocean-Style Augmented Dataset
-------------------------------------------------------------------
✅ Loads base EfficientNet + RandomForest
✅ Trains on new domain-shifted images
✅ Outputs fine-tuned classifier
"""

import os
import cv2
import joblib
import numpy as np
import torch
from tqdm import tqdm
from torchvision import transforms, models
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

AUG_DIR = "data/ocean_augmented_dataset"
CHECKPOINT_DIR = "checkpoints"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print("🚀 Loading EfficientNet base...")
effnet = efficientnet_b0(weights=EfficientNet_B0_Weights.DEFAULT)
effnet.classifier = torch.nn.Identity()
effnet.to(DEVICE).eval()

transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# Load original model & label map
base_clf = joblib.load(os.path.join(CHECKPOINT_DIR, "pollution_type_classifier.pkl"))
label_map = joblib.load(os.path.join(CHECKPOINT_DIR, "label_map.pkl"))
classes = list(label_map.values())

X, y = [], []

print("🌊 Extracting augmented features...")
for i, cls in enumerate(classes):
    cls_folder = os.path.join(AUG_DIR, cls)
    if not os.path.isdir(cls_folder): continue
    for fname in tqdm(os.listdir(cls_folder), desc=f"Fine-tune: {cls}"):
        if not fname.lower().endswith((".jpg", ".png", ".jpeg")): continue
        img = cv2.imread(os.path.join(cls_folder, fname))
        if img is None: continue
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        tensor = transform(img).unsqueeze(0).to(DEVICE)
        with torch.no_grad():
            feat = effnet(tensor).cpu().numpy().flatten()
        X.append(feat)
        y.append(i)

X = np.array(X)
y = np.array(y)

print(f"✅ Loaded {len(X)} augmented embeddings.")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

print("🧠 Fine-tuning RandomForest...")
finetuned_clf = RandomForestClassifier(
    n_estimators=300,
    max_depth=14,
    n_jobs=-1,
    random_state=42
)
finetuned_clf.fit(X_train, y_train)

y_pred = finetuned_clf.predict(X_test)
print("\n📈 Fine-tuned Classification Report:")
print(classification_report(y_test, y_pred, target_names=classes))

joblib.dump(finetuned_clf, os.path.join(CHECKPOINT_DIR, "pollution_type_classifier_finetuned.pkl"))
print("💾 Saved fine-tuned model in checkpoints/pollution_type_classifier_finetuned.pkl")
