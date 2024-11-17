import ray
from ray import tune
from ray.train.torch import TorchTrainer
from ray.train import ScalingConfig
from ultralytics import YOLO


def train_loop_per_worker(config):

    model = YOLO("yolov8n.pt")

    results = model.train(
        data="coco128.yaml",
        epochs=config["epochs"],
        imgsz=config["imgsz"],
        batch=config["batch_size"],
        lr0=config["lr0"],
        device="mps",
    )

    best_map = results.metrics["mAP50"]
    tune.report(mAP50=best_map)


search_space = {
    "batch_size": tune.choice([8, 16]),
    "lr0": tune.loguniform(1e-5, 1e-3),
    "imgsz": tune.choice([640]),
    "epochs": tune.choice([5, 10]),
}

ray.init(address="auto", _temp_dir="/tmp/ray")

print("Preparing to train YOLOv8 on COCO128 dataset")


def distributed_train(config):

    trainer = TorchTrainer(
        train_loop_per_worker=train_loop_per_worker,
        scaling_config=ScalingConfig(
            num_workers=2,
        ),
        train_loop_config=config,
    )

    results = trainer.fit()
    return results


print("Starting hyperparameter search")

tuner = tune.Tuner(
    tune.with_resources(distributed_train, {"cpu": 2}),
    tune_config=tune.TuneConfig(
        metric="mAP50",
        mode="max",
        num_samples=2,
    ),
    param_space=search_space,
)

results = tuner.fit()

best_result = results.get_best_result()
print("best result", best_result)
