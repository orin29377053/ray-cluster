import ray
import random

ray.init(address="auto")


@ray.remote(max_retries=3)
def unstable_task(x):

    if random.random() < 0.5:
        print(f"task failed: {x}")
        raise ValueError("task failed")
    print(f"task succeeded: {x}")
    return x * 2


futures = [unstable_task.remote(i) for i in range(10)]

results = []
for future in futures:
    try:
        result = ray.get(future)
        results.append(result)
    except Exception as e:
        print(f"task failed: {e}")

print("result", results)
