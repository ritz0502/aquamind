# scripts/5_train_unet.py
import os, cv2, torch, torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
import numpy as np
from tqdm import tqdm

# ---------------- CONFIG ----------------
IMG_DIR = "data/synthetic/images"
MASK_DIR = "data/synthetic/masks"
CHECKPOINT = "checkpoints/unet_best.pth"
os.makedirs("checkpoints", exist_ok=True)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
IMG_SIZE = 128
EPOCHS = 5
BATCH_SIZE = 4
LR = 1e-4

# ---------------- DATASET ----------------
class PollutionDataset(Dataset):
    def __init__(self, img_dir, mask_dir):
        self.imgs = [f for f in os.listdir(img_dir) if f.endswith(".jpg")]
        self.img_dir, self.mask_dir = img_dir, mask_dir

    def __getitem__(self, idx):
        name = self.imgs[idx]
        img = cv2.imread(os.path.join(self.img_dir, name))
        mask = cv2.imread(os.path.join(self.mask_dir, name.replace(".jpg", ".png")), 0)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        mask = cv2.resize(mask, (IMG_SIZE, IMG_SIZE))
        img = torch.tensor(img / 255.0).permute(2, 0, 1).float()
        mask = torch.tensor((mask > 127).astype(np.float32)).unsqueeze(0)
        return img, mask

    def __len__(self):
        return len(self.imgs)


# ---------------- U-NET MODEL ----------------
class UNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.enc1 = self.block(3, 64)
        self.enc2 = self.block(64, 128)
        self.enc3 = self.block(128, 256)
        self.enc4 = self.block(256, 512)

        self.pool = nn.MaxPool2d(2)

        self.up1 = self.up_block(512, 256)
        self.up2 = self.up_block(256, 128)
        self.up3 = self.up_block(128, 64)
        self.final = nn.Conv2d(64, 1, kernel_size=1)
        self.sigmoid = nn.Sigmoid()

    def block(self, in_ch, out_ch):
        return nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            nn.ReLU(inplace=True),
        )

    def up_block(self, in_ch, out_ch):
        return nn.Sequential(
            nn.ConvTranspose2d(in_ch, out_ch, kernel_size=2, stride=2),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        x1 = self.enc1(x)
        x2 = self.pool(x1)
        x2 = self.enc2(x2)
        x3 = self.pool(x2)
        x3 = self.enc3(x3)
        x4 = self.pool(x3)
        x4 = self.enc4(x4)

        x = self.up1(x4)
        x = self.up2(x)
        x = self.up3(x)
        x = self.final(x)
        return self.sigmoid(x)


# ---------------- TRAINING LOOP ----------------
def train():
    print("🚀 Loading dataset...")
    ds = PollutionDataset(IMG_DIR, MASK_DIR)
    tr_size = int(0.8 * len(ds))
    val_size = len(ds) - tr_size
    tr_ds, val_ds = random_split(ds, [tr_size, val_size])

    tr_loader = DataLoader(tr_ds, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE)

    model = UNet().to(DEVICE)
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    loss_fn = nn.BCELoss()
    best_loss = float("inf")

    print(f"🧠 Training on {DEVICE} with {len(tr_loader)} batches per epoch")
    for epoch in range(1, EPOCHS + 1):
        model.train()
        train_loss = 0
        for imgs, masks in tqdm(tr_loader, desc=f"Epoch {epoch}/{EPOCHS}"):
            imgs, masks = imgs.to(DEVICE), masks.to(DEVICE)
            preds = model(imgs)
            loss = loss_fn(preds, masks)
            opt.zero_grad()
            loss.backward()
            opt.step()
            train_loss += loss.item()

        val_loss = 0
        model.eval()
        with torch.no_grad():
            for imgs, masks in val_loader:
                imgs, masks = imgs.to(DEVICE), masks.to(DEVICE)
                preds = model(imgs)
                loss = loss_fn(preds, masks)
                val_loss += loss.item()

        val_loss /= len(val_loader)
        train_loss /= len(tr_loader)
        print(f"📘 Epoch {epoch}: train={train_loss:.4f} val={val_loss:.4f}")

        if val_loss < best_loss:
            best_loss = val_loss
            torch.save(model.state_dict(), CHECKPOINT)
            print("💾 Saved best model ✅")

    print("✅ Training complete — best model stored in checkpoints/unet_best.pth")


# ---------------- ENTRY ----------------
if __name__ == "__main__":
    train()
