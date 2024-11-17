import os
import requests
from zipfile import ZipFile
import yaml  # Used for parsing YAML files
import shutil  # Used for file operations

yaml_url = (
    "https://raw.githubusercontent.com/ultralytics/yolov5/master/data/coco128.yaml"
)
yaml_file = "datasets/coco128.yaml"

os.makedirs(os.path.dirname(yaml_file), exist_ok=True)

print("Downloading coco128.yaml...")
response = requests.get(yaml_url)
if response.status_code == 200:
    with open(yaml_file, "w") as f:
        f.write(response.text)
    print(f"coco128.yaml has been saved to {yaml_file}")
else:
    print(f"Download failed, status code: {response.status_code}")
    exit(1)

print("Parsing coco128.yaml...")
with open(yaml_file, "r") as f:
    yaml_data = yaml.safe_load(f)

dataset_url = yaml_data.get("download")
if not dataset_url:
    print("Unable to find the dataset download link in coco128.yaml")
    exit(1)

output_zip = "datasets/coco128.zip"

if not os.path.exists(output_zip):
    print("Downloading coco128 dataset...")
    response = requests.get(dataset_url)
    if response.status_code == 200:
        with open(output_zip, "wb") as f:
            f.write(response.content)
        print(f"Dataset has been downloaded and saved as {output_zip}")
    else:
        print(f"Dataset download failed, status code: {response.status_code}")
        exit(1)
else:
    print(f"{output_zip} already exists, skipping download.")

output_dir = "datasets/coco128"
if not os.path.exists(output_dir):
    print("Extracting files")
    with ZipFile(output_zip, "r") as zip_ref:
        for member in zip_ref.namelist():
            # Remove the top-level directory 'coco128/'
            member_path = member.split("/", 1)[-1] if "/" in member else member
            if not member_path:
                continue  # Skip empty paths
            target_path = os.path.join(output_dir, member_path)
            if member.endswith("/"):
                # Create directory
                os.makedirs(target_path, exist_ok=True)
            else:
                # Create file
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                with zip_ref.open(member) as source, open(target_path, "wb") as target:
                    shutil.copyfileobj(source, target)
    print(f"Files have been extracted to: {output_dir}")
else:
    print(f"Files have been extracted to: {output_dir}")
