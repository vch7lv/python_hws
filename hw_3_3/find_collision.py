import numpy as np
from matrix import Matrix


def find_collision(max_sum: int = 5, size: int = 2):
    for s in range(max_sum * size * size + 1):
        seen = {}
        for _ in range(1000):
            arr = np.random.randint(0, max_sum + 1, (size, size))
            if arr.sum() != s:
                continue
            M = Matrix(arr)
            h = hash(M)
            if h not in seen:
                seen[h] = M
            elif not np.array_equal(seen[h]._data, arr):
                return seen[h], M
    return None, None


if __name__ == "__main__":
    np.random.seed(42)
    A, C = find_collision(max_sum=3, size=2)
    if A is not None:
        print("Collision found:")
        print("A:", A._data, "hash=", hash(A))
        print("C:", C._data, "hash=", hash(C))
        print("hash(A)==hash(C):", hash(A) == hash(C))
        print("A!=C:", A != C)
    else:
        A = Matrix(np.array([[1, 0], [0, 0]]))
        C = Matrix(np.array([[0, 1], [0, 0]]))
        print("Known collision: A sum=1, C sum=1, shape (2,2)")
        print("hash(A)==hash(C):", hash(A) == hash(C))
