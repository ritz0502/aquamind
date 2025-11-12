# scripts/8_evaluate_model.py
import os, cv2, json, torch, joblib
import numpy as np
import matplotlib.pyplot as plt
from transformers import pipeline
from tqdm import tqdm
from scripts.train_unet import UNet

# Paths
IMG_DIR = "data/test_images"
OUTPUT_DIR = "outputs/eval_results"
CHECKPOINT_UNET = "checkpoints/unet_best.pth"
CHECKPOINT_CLF = "checkpoints/pollution_type_classifier.pkl"
LABEL_MAP_PATH = "checkpoints/label_map.pkl"

os.makedirs(OUTPUT_DIR, exist_ok=True)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
unet = UNet().to(DEVICE)
unet.load_state_dict(torch.load(CHECKPOINT_UNET, map_location=DEVICE))
unet.eval()

clf = joblib.load(CHECKPOINT_CLF)
label_map = joblib.load(LABEL_MAP_PATH)
gen = pipeline("text-generation", model="distilgpt2", device=0 if DEVICE == "cuda" else -1)

def infer_single_image(img_path):
    img = cv2.imread(img_path)
    inp = cv2.resize(img, (256, 256))
    tensor = torch.tensor(inp / 255.).permute(2, 0, 1).unsqueeze(0).float().to(DEVICE)

    with torch.no_grad():
        mask_pred = unet(tensor)[0, 0].cpu().numpy()

    mask_bin = (mask_pred > 0.5).astype(np.uint8)
    mask_vis = (mask_bin * 255).astype(np.uint8)
    mask_resized = cv2.resize(mask_vis, (img.shape[1], img.shape[0]))

    overlay = img.copy()
    overlay[mask_resized > 127] = (0.4 * overlay[mask_resized > 127] + 0.6 * np.array([255, 0, 0])).astype(np.uint8)

    feats = [inp[:, :, 0].mean(), inp[:, :, 1].mean(), inp[:, :, 2].mean()]
    pred = clf.predict([feats])[0]
    pollution_type = label_map[int(pred)]

    text = f"The image shows {pollution_type} pollution. Suggest an immediate cleanup measure."
    explanation = gen(text, max_new_tokens=50)[0]["generated_text"]

    result = {
        "image": img_path,
        "predicted_type": pollution_type,
        "explanation": explanation,
        "mask_path": os.path.join(OUTPUT_DIR, os.path.basename(img_path).replace(".jpg", "_mask.png"))
    }

    cv2.imwrite(result["mask_path"], mask_resized)
    return img, overlay, result

def visualize_results():
    images = [os.path.join(IMG_DIR, f) for f in os.listdir(IMG_DIR) if f.lower().endswith(('.jpg','.png'))]
    all_results = []

    for img_path in tqdm(images, desc="🔍 Evaluating test images"):
        img, overlay, res = infer_single_image(img_path)
        all_results.append(res)

        plt.figure(figsize=(10,4))
        plt.subplot(1,2,1)
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.title("Original Image")
        plt.axis("off")

        plt.subplot(1,2,2)
        plt.imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
        plt.title(f"Predicted: {res['predicted_type']}")
        plt.axis("off")

        plt.suptitle("Marine Pollution Detection Result", fontsize=13)
        plt.tight_layout()
        save_path = os.path.join(OUTPUT_DIR, os.path.basename(img_path).replace(".jpg", "_result.png"))
        plt.savefig(save_path)
        plt.close()

    with open(os.path.join(OUTPUT_DIR, "results_summary.json"), "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n✅ Evaluation complete. Results saved in {OUTPUT_DIR}/")

if __name__ == "__main__":
    visualize_results()
