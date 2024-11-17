import os
import requests
from zipfile import ZipFile
import yaml  # Used for parsing YAML files

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
    print("Unable to find dataset URL in coco128.yaml")
    exit(1)

output_zip = "datasets/coco128.zip"  # Update the path to include 'datasets/'

if not os.path.exists(output_zip):
    print("Downloading coco128 dataset...")
    response = requests.get(dataset_url)
    if response.status_code == 200:
        with open(output_zip, "wb") as f:
            f.write(response.content)
        print(f"Dataset downloaded and saved as {output_zip}")
    else:
        print(f"Dataset download failed, status code: {response.status_code}")
        exit(1)
else:
    print(f"{output_zip} already exists. Skipping download.")

output_dir = "datasets/coco128"
if not os.path.exists(output_dir):
    print("Extracting files...")
    with ZipFile(output_zip, "r") as zip_ref:
        zip_ref.extractall(output_dir)
    print(f"Files extracted to: {output_dir}")
else:
    print(f"Files already extracted to: {output_dir}")
