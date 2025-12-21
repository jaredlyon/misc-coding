from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from pathlib import Path
from PIL import Image

image_folder = Path("images_out")
output_file = image_folder / "timelapse.mp4"
seconds_per_image = 1

images = sorted(image_folder.glob("snapshot-*.jpg"))
if not images:
    raise ValueError(f"No images found in {image_folder} matching snapshot-*.jpg")

resized_folder = image_folder / "resized"
resized_folder.mkdir(exist_ok=True)

first_img = Image.open(images[0])
target_size = first_img.size

resized_image_paths = []
for img_path in images:
    img = Image.open(img_path)
    if img.size != target_size:
        img = img.resize(target_size)
    resized_path = resized_folder / img_path.name
    img.save(resized_path)
    resized_image_paths.append(str(resized_path))

fps = 1 / seconds_per_image
clip = ImageSequenceClip(resized_image_paths, fps=fps)
clip.write_videofile(str(output_file), codec="libx264")

print(f"Timelapse created: {output_file}")

# pip install moviepy