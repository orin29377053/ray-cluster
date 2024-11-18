import ray
import random

ray.init(address="auto", _metrics_export_port=8080)


@ray.remote
def compute(x):
    result = x * x
    print(f"Computing {x} -> {result}")
    return result


def main():

    numbers = [random.randint(1, 10) for _ in range(5)]
    print("Input numbers:", numbers)

    try:
        futures = [compute.remote(num) for num in numbers]
        results = ray.get(futures)
        print("Results:", results)
    finally:
        ray.shutdown()


if __name__ == "__main__":
    main()
