import math
import os
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def _integrate_chunk(f, a, b, n_iter, chunk_id, n_jobs):
    step = (b - a) / n_iter
    chunk_size = n_iter // n_jobs
    start_i = chunk_id * chunk_size
    end_i = start_i + chunk_size if chunk_id < n_jobs - 1 else n_iter
    acc = 0.0
    for i in range(start_i, end_i):
        acc += f(a + i * step) * step
    return acc


def integrate(f, a, b, *, n_jobs=1, n_iter=10000000, executor_class=None):
    if n_jobs <= 1 or executor_class is None:
        acc = 0.0
        step = (b - a) / n_iter
        for i in range(n_iter):
            acc += f(a + i * step) * step
        return acc
    with executor_class(max_workers=n_jobs) as ex:
        futures = [
            ex.submit(_integrate_chunk, f, a, b, n_iter, j, n_jobs)
            for j in range(n_jobs)
        ]
        return sum(fut.result() for fut in futures)


def main():
    cpu_num = os.cpu_count() or 1
    n_jobs_range = list(range(1, cpu_num * 2 + 1))
    results = []

    for n_jobs in n_jobs_range:
        start = time.perf_counter()
        integrate(math.cos, 0, math.pi / 2, n_jobs=n_jobs, executor_class=ThreadPoolExecutor)
        t_thread = time.perf_counter() - start

        start = time.perf_counter()
        integrate(math.cos, 0, math.pi / 2, n_jobs=n_jobs, executor_class=ProcessPoolExecutor)
        t_process = time.perf_counter() - start

        results.append((n_jobs, t_thread, t_process))

    lines = [
        "n_jobs  ThreadPoolExecutor(s)  ProcessPoolExecutor(s)",
        "-" * 52,
    ]
    for n_jobs, t_thread, t_process in results:
        lines.append(f"{n_jobs:6}  {t_thread:20.4f}  {t_process:22.4f}")

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts", "comparison.txt")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write("\n".join(lines))

    print("\n".join(lines))


if __name__ == "__main__":
    main()
