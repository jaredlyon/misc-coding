import os
import re
from PIL import Image, ImageDraw, ImageFont

INPUT_DIR = "images"
OUTPUT_DIR = "images_out"

FONT_PATH = r"C:\Windows\Fonts\segoeui.ttf"  # change if needed
FONT_SCALE = 0.04        # % of image width (bigger = larger text)
PADDING_RATIO = 0.4      # padding relative to font size
BAR_OPACITY = 220        # 0–255

DATE_REGEX = re.compile(r"\d{4}-\d{2}-\d{2}")

os.makedirs(OUTPUT_DIR, exist_ok=True)

for filename in os.listdir(INPUT_DIR):
    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    match = DATE_REGEX.search(filename)
    if not match:
        print(f"Skipping (no date found): {filename}")
        continue

    date_text = match.group()

    img = Image.open(os.path.join(INPUT_DIR, filename)).convert("RGBA")
    draw = ImageDraw.Draw(img)

    img_w, img_h = img.size

    font_size = int(img_w * FONT_SCALE)
    font = ImageFont.truetype(FONT_PATH, font_size)

    padding = int(font_size * PADDING_RATIO)

    text_bbox = draw.textbbox((0, 0), date_text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]

    bar_w = text_w + 2 * padding
    bar_h = text_h + 2 * padding

    x = img_w - bar_w
    y = img_h - bar_h

    bar = Image.new("RGBA", (bar_w, bar_h), (0, 0, 0, BAR_OPACITY))
    img.paste(bar, (x, y), bar)

    text_x = x + padding - text_bbox[0]
    text_y = y + padding - text_bbox[1]

    draw.text(
        (text_x, text_y),
        date_text,
        fill=(255, 255, 255),
        font=font,
    )

    output_path = os.path.join(OUTPUT_DIR, filename)
    img.convert("RGB").save(output_path)

print("All images processed successfully.")


# pip install pillow