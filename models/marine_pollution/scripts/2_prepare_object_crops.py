# from rembg import remove
# from PIL import Image
# import os
# from tqdm import tqdm

# INPUT_DIR = "training_dataset"
# OUTPUT_DIR = "data/clean_crops"
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# for cls in os.listdir(INPUT_DIR):
#     cls_path = os.path.join(INPUT_DIR, cls)
#     if not os.path.isdir(cls_path): continue
#     out_cls = os.path.join(OUTPUT_DIR, cls)
#     os.makedirs(out_cls, exist_ok=True)
#     print(f"🔹 Cleaning {cls} ...")

#     for fname in tqdm(os.listdir(cls_path)):
#         if not fname.lower().endswith((".jpg", ".png", ".jpeg")):
#             continue
#         inp = Image.open(os.path.join(cls_path, fname)).convert("RGBA")
#         result = remove(inp)
#         result.save(os.path.join(out_cls, fname))

# print("✅ Clean transparent crops created.")







# import os, subprocess
# from tqdm import tqdm
# from PIL import Image

# INPUT_DIR = "training_dataset"
# OUTPUT_DIR = "data/clean_crops"
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # Ensure rembg is installed
# try:
#     import rembg
# except ImportError:
#     print("⚙️ Installing rembg...")
#     subprocess.run(["pip", "install", "rembg"], check=True)

# def remove_bg_cli(input_path, output_path):
#     # Use rembg CLI (avoids numba import issues)
#     cmd = ["rembg", "i", input_path, output_path]
#     subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# for cls in os.listdir(INPUT_DIR):
#     cls_path = os.path.join(INPUT_DIR, cls)
#     if not os.path.isdir(cls_path): continue
#     out_cls = os.path.join(OUTPUT_DIR, cls)
#     os.makedirs(out_cls, exist_ok=True)
#     print(f"🔹 Cleaning {cls} ...")

#     for fname in tqdm(os.listdir(cls_path)):
#         if not fname.lower().endswith((".jpg", ".png", ".jpeg")):
#             continue
#         inp = os.path.join(cls_path, fname)
#         outp = os.path.join(out_cls, os.path.splitext(fname)[0] + ".png")
#         remove_bg_cli(inp, outp)

# print("✅ Backgrounds removed and transparent PNGs saved to data/clean_crops/")





















import os
import numpy as np
from tqdm import tqdm
from PIL import Image
from rembg import new_session, remove

INPUT_DIR = "training_dataset"
OUTPUT_DIR = "data/clean_crops"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load model once
print("⚙️ Loading rembg session (this may take 30s the first time)...")
session = new_session("u2netp")  # lightweight model also works: "u2netp"

def remove_bg_fast(input_path, output_path):
    """Remove background using single rembg session."""
    try:
        with open(input_path, "rb") as i:
            result = remove(i.read(), session=session)
        with open(output_path, "wb") as o:
            o.write(result)
    except Exception as e:
        print(f"❌ Error processing {input_path}: {e}")

# Loop over classes
for cls in os.listdir(INPUT_DIR):
    cls_path = os.path.join(INPUT_DIR, cls)
    if not os.path.isdir(cls_path):
        continue

    out_cls = os.path.join(OUTPUT_DIR, cls)
    os.makedirs(out_cls, exist_ok=True)

    print(f"\n🔹 Cleaning {cls} ({len(os.listdir(cls_path))} images)...")

    for fname in tqdm(os.listdir(cls_path)):
        if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        inp = os.path.join(cls_path, fname)
        outp = os.path.join(out_cls, os.path.splitext(fname)[0] + ".png")

        if os.path.exists(outp):  # skip already processed
            continue

        remove_bg_fast(inp, outp)

print("✅ Background removal completed. Output in data/clean_crops/")
