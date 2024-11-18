# Changelog


## [2024-11-14]
- Initial commit of the project.
### Added
- Initial project setup with the following files:
  - **.gitignore**: Added to ignore Python cache files, virtual environments, IDE configurations, and other build artifacts.
  - **CHANGELOG.md**: Created to track changes in the project.
  - **parallel_compute.py**: Added a script for parallel computation using Ray.
  - **ray-cluster.yaml**: Configuration file for setting up a Ray cluster.
  - **unstable_task.py**: Script demonstrating the use of Ray with a task that may fail.

## [2024-11-15]
### Features
- Updated entrypoint script to support role-based initialization for Ray cluster.
- Increased minimum replicas for worker nodes in the Ray cluster configuration.
- Changed Docker image to a custom version for both head and worker nodes.
- Enhanced logging in `parallel_compute.py` to indicate computation progress.
- Adjusted failure threshold in `unstable_task.py` to increase task failure rate.


## [2024-11-17]
### Added
- **download_dataset.py**: Added a script to download and extract the COCO128 dataset from a YAML configuration file.
  - Downloads `coco128.yaml` and retrieves the dataset URL.
  - Downloads the dataset and extracts it to the specified directory.
  
- **training.py**: Added a script for training the YOLOv8 model using the COCO128 dataset.
  - Implements a distributed training loop with hyperparameter tuning using Ray Tune.
  - Reports the mean Average Precision (mAP50) metric during training.

## [2024-11-18,19]
### Added
- **Monitoring**: Added Grafana and Prometheus to the Ray cluster and successfully retrieved metrics.
- **Other Tasks**: Adjusted the system configuration and updated the README file.