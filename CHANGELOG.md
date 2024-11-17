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