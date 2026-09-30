import os
import json
from PIL import Image, ImageOps

OBJ_DIR = 'FBXs'
output_file = os.path.join(OBJ_DIR, 'modelList.json')
GALLERY_DIRS = ('Doodle', 'Icons', 'Halfbodies', 'Fullbodies')
GALLERY_OUTPUT = 'galleryList.js'
THUMBNAIL_ROOT = 'GalleryThumbnails'
THUMBNAIL_SIZE = (512, 512)
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.avif', '.bmp', '.svg'}

models = []

# Walk through each folder inside OBJs/
for folder in os.listdir(OBJ_DIR):
    folder_path = os.path.join(OBJ_DIR, folder)
    if os.path.isdir(folder_path):
        obj_file = os.path.join(folder_path, f'{folder}.fbx')
        if os.path.isfile(obj_file):
            models.append(folder)

# Save the list as JSON
with open(output_file, 'w') as f:
    json.dump(models, f, indent=2)

print(f"Generated model list with {len(models)} entries.")

galleries = {}
thumbnail_count = 0
for folder in GALLERY_DIRS:
    if not os.path.isdir(folder):
        galleries[folder] = []
        continue

    gallery_entries = []
    thumbnail_folder = os.path.join(THUMBNAIL_ROOT, folder)
    os.makedirs(thumbnail_folder, exist_ok=True)

    filenames = sorted(
        (
            filename
            for filename in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, filename))
            and os.path.splitext(filename)[1].lower() in IMAGE_EXTENSIONS
        ),
        key=str.casefold,
    )

    for filename in filenames:
        source_path = os.path.join(folder, filename)
        thumbnail_name = f'{filename}.webp'
        thumbnail_path = os.path.join(thumbnail_folder, thumbnail_name)

        try:
            with Image.open(source_path) as source_image:
                thumbnail = ImageOps.exif_transpose(source_image)
                thumbnail.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
                has_alpha = 'A' in thumbnail.getbands() or 'transparency' in thumbnail.info
                thumbnail = thumbnail.convert('RGBA' if has_alpha else 'RGB')
                thumbnail.save(thumbnail_path, 'WEBP', quality=82, method=6)
            thumbnail_count += 1
        except (OSError, ValueError) as error:
            print(f'Could not create a thumbnail for {source_path}: {error}')
            thumbnail_name = None

        gallery_entries.append({
            'file': filename,
            'thumbnail': thumbnail_name,
        })

    galleries[folder] = gallery_entries

with open(GALLERY_OUTPUT, 'w', encoding='utf-8') as gallery_file:
    gallery_file.write('window.commissionGallery = ')
    json.dump(galleries, gallery_file, indent=2, ensure_ascii=False)
    gallery_file.write(';\n')

print(f"Generated gallery list for {sum(map(len, galleries.values()))} images and {thumbnail_count} thumbnails.")
