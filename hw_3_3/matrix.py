from __future__ import annotations

import os
from typing import Dict, Tuple

import numpy as np

from hash_mixin import HashMixin


def _matrix_format(arr: np.ndarray) -> str:
    return "\n".join(" ".join(str(int(x)) for x in row) for row in arr)


_matmul_cache: Dict[Tuple[int, int], Matrix] = {}


class Matrix(HashMixin):

    def __init__(self, data: np.ndarray):
        self._data = np.asarray(data, dtype=np.int64)

    @property
    def shape(self):
        return self._data.shape

    def __add__(self, other: "Matrix") -> "Matrix":
        if not isinstance(other, Matrix):
            return NotImplemented
        if self._data.shape != other._data.shape:
            raise ValueError(f"Addition: shape mismatch {self._data.shape} vs {other._data.shape}")
        return Matrix(self._data + other._data)

    def __mul__(self, other: "Matrix") -> "Matrix":
        if not isinstance(other, Matrix):
            return NotImplemented
        if self._data.shape != other._data.shape:
            raise ValueError(f"*: shape mismatch {self._data.shape} vs {other._data.shape}")
        return Matrix(self._data * other._data)

    def __matmul__(self, other: "Matrix") -> "Matrix":
        if not isinstance(other, Matrix):
            return NotImplemented
        a, b = self._data, other._data
        if a.shape[1] != b.shape[0]:
            raise ValueError(f"@: incompatible shapes {a.shape} @ {b.shape}")
        key = (hash(self), hash(other))
        if key in _matmul_cache:
            return _matmul_cache[key]
        res = Matrix(a @ b)
        _matmul_cache[key] = res
        return res

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return NotImplemented
        return np.array_equal(self._data, other._data)

    def __hash__(self) -> int:
        return HashMixin.__hash__(self)

    def __str__(self) -> str:
        return _matrix_format(self._data)

    def to_file(self, path: str) -> None:
        d = os.path.dirname(path)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(path, "w") as f:
            f.write(self.__str__())
            f.write("\n")


def main() -> None:
    A = Matrix(np.array([[1, 0], [0, 0]]))
    C = Matrix(np.array([[0, 1], [0, 0]]))
    B = Matrix(np.eye(2, dtype=np.int64))
    D = Matrix(np.eye(2, dtype=np.int64))

    assert hash(A) == hash(C), "hash(A) == hash(C)"
    assert A != C, "A != C"
    assert B == D, "B == D"
    AB = A @ B
    CD = Matrix(C._data @ D._data)
    assert not np.array_equal(AB._data, CD._data), "A @ B != C @ D"

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts")
    os.makedirs(out, exist_ok=True)
    A.to_file(os.path.join(out, "A.txt"))
    B.to_file(os.path.join(out, "B.txt"))
    C.to_file(os.path.join(out, "C.txt"))
    D.to_file(os.path.join(out, "D.txt"))
    AB.to_file(os.path.join(out, "AB.txt"))
    CD.to_file(os.path.join(out, "CD.txt"))
    with open(os.path.join(out, "hash.txt"), "w") as f:
        f.write(f"hash(AB) = {hash(AB)}\n")
        f.write(f"hash(CD) = {hash(CD)}\n")


if __name__ == "__main__":
    main()
