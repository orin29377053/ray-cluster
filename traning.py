import ray
from ray import tune
from ray.train.torch import TorchTrainer
from ray.train import ScalingConfig, report
from ultralytics import YOLO
import logging
import torch


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train_loop_per_worker(config):
    try:
        logger.info(f"Starting training with config: {config}")

   
        device = "cpu"
        if torch.backends.mps.is_available():
            device = "mps"
        logger.info(f"Using device: {device}")


        model = YOLO("yolov8n.pt")
        logger.info("Model loaded successfully")

 
        for epoch in range(config["epochs"]):
            results = model.train(
                data="coco128.yaml",
                epochs=1,  # 每次跑一個 epoch
                imgsz=config["imgsz"],
                batch=config["batch_size"],
                lr0=config["lr0"],
                device=device,
                plots=False,
                save=False,
            )


            best_map = results.results_dict["metrics/mAP50(B)"]
            logger.info(f"Epoch {epoch + 1} mAP50: {best_map}")

   
            report({
                "epoch": epoch + 1,
                "mAP50": float(best_map),
                "batch_size": config["batch_size"],
                "lr0": config["lr0"],
                "imgsz": config["imgsz"],
            })

    except Exception as e:
        logger.error(f"Error in training loop: {str(e)}", exc_info=True)
        raise


def main():
    try:

        ray.init(address="auto", _temp_dir="/tmp/ray", logging_level=logging.INFO)
        logger.info("Ray initialized successfully")

        
        search_space = {
            "batch_size": 4,
            "lr0": 0.001,
            "imgsz": 64, 
            "epochs": 1,  
        }

        logger.info(f"Using search space: {search_space}")


        def distributed_train(config):
            trainer = TorchTrainer(
                train_loop_per_worker=train_loop_per_worker,
                scaling_config=ScalingConfig(
                    num_workers=1, use_gpu=False
                ),
                train_loop_config=config,
            )

            results = trainer.fit()
            logger.info(f"Training results: {results.metrics}")


            return {"mAP50": results.metrics.get("mAP50", 0)}


        tuner = tune.Tuner(
            tune.with_resources(distributed_train, {"cpu": 2}),
            param_space=search_space,
            tune_config=tune.TuneConfig(
                num_samples=1,
                metric="mAP50",
                mode="max",
            ),
        )


        results = tuner.fit()


        best_result = results.get_best_result()
        logger.info(f"Best result: {best_result}")

    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)
        raise
    finally:
        ray.shutdown()
        logger.info("Ray shut down")


if __name__ == "__main__":
    main()
