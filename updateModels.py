import os
import json

OBJ_DIR = 'FBXs'
output_file = os.path.join(OBJ_DIR, 'modelList.json')

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
