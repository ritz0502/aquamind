import torch, cv2, numpy as np, os
from torchvision import transforms
from scripts.train_unet import UNet

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model = UNet().to(DEVICE)
model.load_state_dict(torch.load("checkpoints/unet_best.pth", map_location=DEVICE))
model.eval()

def segment_image(img_path):
    img = cv2.imread(img_path)
    orig = img.copy()
    img = cv2.resize(img, (256, 256)) / 255.0
    tensor = torch.tensor(img.transpose(2,0,1)).unsqueeze(0).float().to(DEVICE)
    with torch.no_grad():
        pred = model(tensor)[0,0].cpu().numpy()
    mask = (pred > 0.5).astype(np.uint8)*255
    mask = cv2.resize(mask, (orig.shape[1], orig.shape[0]))
    return mask

img_path = "data/test_images/test.jpg"
mask = segment_image(img_path)
cv2.imwrite("outputs/segmented_mask.png", mask)
print("✅ Saved segmented mask.")
