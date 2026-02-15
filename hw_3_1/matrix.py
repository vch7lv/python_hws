import os
import numpy as np


def _matrix_format(arr: np.ndarray) -> str:
    return "\n".join(" ".join(str(int(x)) for x in row) for row in arr)


class Matrix:

    def __init__(self, data: np.ndarray):
        self._data = np.asarray(data, dtype=np.int64)

    @property
    def shape(self):
        return self._data.shape

    def __add__(self, other: "Matrix") -> "Matrix":
        if not isinstance(other, Matrix):
            return NotImplemented
        if self._data.shape != other._data.shape:
            raise ValueError(
                f"Addition: shape mismatch {self._data.shape} vs {other._data.shape}"
            )
        return Matrix(self._data + other._data)

    def __mul__(self, other: "Matrix") -> "Matrix":
        if not isinstance(other, Matrix):
            return NotImplemented
        if self._data.shape != other._data.shape:
            raise ValueError(
                f"Component-wise *: shape mismatch {self._data.shape} vs {other._data.shape}"
            )
        return Matrix(self._data * other._data)

    def __matmul__(self, other: "Matrix") -> "Matrix":
        if not isinstance(other, Matrix):
            return NotImplemented
        a, b = self._data, other._data
        if a.shape[1] != b.shape[0]:
            raise ValueError(
                f"Matrix @: incompatible shapes {a.shape} @ {b.shape}"
            )
        return Matrix(a @ b)

    def __str__(self) -> str:
        return _matrix_format(self._data)

    def to_file(self, path: str) -> None:
        with open(path, "w") as f:
            f.write(self.__str__())
            f.write("\n")


def main() -> None:
    np.random.seed(0)
    a = np.random.randint(0, 10, (10, 10))
    b = np.random.randint(0, 10, (10, 10))
    A, B = Matrix(a), Matrix(b)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts")
    os.makedirs(out_dir, exist_ok=True)
    (A + B).to_file(os.path.join(out_dir, "matrix+.txt"))
    (A * B).to_file(os.path.join(out_dir, "matrix*.txt"))
    (A @ B).to_file(os.path.join(out_dir, "matrix@.txt"))


if __name__ == "__main__":
    main()
