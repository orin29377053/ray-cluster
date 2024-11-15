import ray
import random

ray.init(address="auto")
# ray.init(num_cpus=4)


@ray.remote
def compute(x):
    print(f"computing {x}")
    return x * x


numbers = [random.randint(1, 100) for _ in range(100)]

futures = [compute.remote(num) for num in numbers]

results = ray.get(futures)

print("result", results)
