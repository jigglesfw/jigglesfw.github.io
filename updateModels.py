import os
import json

OBJ_DIR = 'FBXs'
output_file = os.path.join(OBJ_DIR, 'modelList.json')
GALLERY_DIRS = ('Doodle', 'Icons', 'Halfbodies', 'Fullbodies')
GALLERY_OUTPUT = 'galleryList.js'
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
for folder in GALLERY_DIRS:
    if not os.path.isdir(folder):
        galleries[folder] = []
        continue

    galleries[folder] = sorted(
        (
            filename
            for filename in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, filename))
            and os.path.splitext(filename)[1].lower() in IMAGE_EXTENSIONS
        ),
        key=str.casefold,
    )

with open(GALLERY_OUTPUT, 'w', encoding='utf-8') as gallery_file:
    gallery_file.write('window.commissionGallery = ')
    json.dump(galleries, gallery_file, indent=2, ensure_ascii=False)
    gallery_file.write(';\n')

print(f"Generated gallery list for {sum(map(len, galleries.values()))} images.")
