import os
import threading
import multiprocessing
import time


def fib(n: int) -> int:
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def run_sync(n: int, count: int = 10) -> float:
    start = time.perf_counter()
    for _ in range(count):
        fib(n)
    return time.perf_counter() - start


def _run_fib(n: int) -> None:
    fib(n)


def run_threading(n: int, count: int = 10) -> float:
    start = time.perf_counter()
    threads = [threading.Thread(target=_run_fib, args=(n,)) for _ in range(count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return time.perf_counter() - start


def run_multiprocessing(n: int, count: int = 10) -> float:
    start = time.perf_counter()
    procs = [multiprocessing.Process(target=_run_fib, args=(n,)) for _ in range(count)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    return time.perf_counter() - start


def main() -> None:
    n = 300000
    count = 10

    t_sync = run_sync(n, count)
    t_thread = run_threading(n, count)
    t_proc = run_multiprocessing(n, count)

    lines = [
        f"fib(n) with n={n}, {count} runs",
        "",
        "Synchronous (sequential):  {:.3f} s".format(t_sync),
        "Threading (10 threads):   {:.3f} s".format(t_thread),
        "Multiprocessing (10 proc): {:.3f} s".format(t_proc),
        "",
    ]
    text = "\n".join(lines)

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts", "results.txt")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write(text)

    print(text)


if __name__ == "__main__":
    main()
