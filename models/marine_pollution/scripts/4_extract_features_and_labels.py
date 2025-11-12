# scripts/4_extract_features_and_labels.py
import os, cv2, numpy as np, joblib
from tqdm import tqdm

IMG_DIR = "data/synthetic/images"
MASK_DIR = "data/synthetic/masks"
OUT_PATH = "checkpoints/features_labels.pkl"
os.makedirs("checkpoints", exist_ok=True)

def extract_features(image, mask):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    feat = [
        hsv[:,:,0].mean(), hsv[:,:,1].mean(), hsv[:,:,2].mean(),
        hsv[:,:,0].std(), hsv[:,:,1].std(), hsv[:,:,2].std(),
        np.count_nonzero(mask)/(mask.size + 1e-9)
    ]
    return np.array(feat, dtype=np.float32)

features, labels = [], []
label_map = {"plastic": 0, "paper": 1, "trash": 2 , "metal": 3, "glass": 4  }

for fname in tqdm(os.listdir(IMG_DIR), desc="Extracting features"):
    if not fname.endswith(".jpg"): continue
    mask_path = os.path.join(MASK_DIR, fname.replace(".jpg", ".png"))
    if not os.path.exists(mask_path): continue
    img = cv2.imread(os.path.join(IMG_DIR, fname))
    mask = cv2.imread(mask_path, 0)
    cls = fname.split("_")[0]
    features.append(extract_features(img, mask))
    labels.append(label_map[cls])

joblib.dump((np.array(features), np.array(labels)), OUT_PATH)
print(f"✅ Saved {len(features)} feature vectors to {OUT_PATH}")
