# scripts/3_generate_synthetic_dataset.py
import os, random, cv2, numpy as np
from tqdm import tqdm
from PIL import Image

BG_DIR = "data/clean_backgrounds"
OBJ_DIR = "data/clean_crops"
OUT_IMG = "data/synthetic/images"
OUT_MASK = "data/synthetic/masks"
os.makedirs(OUT_IMG, exist_ok=True)
os.makedirs(OUT_MASK, exist_ok=True)

CLASSES = ["plastic", "paper", "trash", "metal", "glass"]
IMAGES_PER_CLASS = 200  # total = 600 synthetic images

def overlay_object(bg, obj, scale):
    obj = obj.convert("RGBA")
    w, h = bg.size
    new_size = (int(obj.width * scale), int(obj.height * scale))
    obj = obj.resize(new_size, Image.LANCZOS)
    x = random.randint(0, max(1, w - new_size[0]))
    y = random.randint(0, max(1, h - new_size[1]))
    bg.paste(obj, (x, y), obj)
    return bg, (x, y, new_size[0], new_size[1])

def make_mask(h, w, rects):
    mask = np.zeros((h, w), dtype=np.uint8)
    for (x, y, ow, oh) in rects:
        cv2.rectangle(mask, (x, y), (x + ow, y + oh), 255, -1)
    return mask

bgs = [os.path.join(BG_DIR, f) for f in os.listdir(BG_DIR) if f.endswith(('.jpg', '.png'))]
count = 0

for cls in CLASSES:
    cls_dir = os.path.join(OBJ_DIR, cls)
    obj_imgs = [os.path.join(cls_dir, f) for f in os.listdir(cls_dir) if f.endswith(".png")]
    for i in tqdm(range(IMAGES_PER_CLASS), desc=f"🧩 Generating {cls} synthetic images"):
        bg_path = random.choice(bgs)
        bg = Image.open(bg_path).convert("RGB").resize((512, 512))
        rects = []
        for _ in range(random.randint(2, 4)):
            obj = Image.open(random.choice(obj_imgs))
            bg, rect = overlay_object(bg, obj, random.uniform(0.3, 0.7))
            rects.append(rect)
        bg_np = cv2.cvtColor(np.array(bg), cv2.COLOR_RGB2BGR)
        mask = make_mask(512, 512, rects)
        cv2.imwrite(os.path.join(OUT_IMG, f"{cls}_{count}.jpg"), bg_np)
        cv2.imwrite(os.path.join(OUT_MASK, f"{cls}_{count}.png"), mask)
        count += 1

print(f"✅ Generated {count} balanced synthetic image-mask pairs in data/synthetic/")
