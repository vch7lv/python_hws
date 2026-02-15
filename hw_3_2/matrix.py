import os
import numbers
import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin

from mixins import FileWriterMixin, GetterSetterMixin, StrMixin


class Matrix(
    NDArrayOperatorsMixin,
    StrMixin,
    FileWriterMixin,
    GetterSetterMixin,
):

    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __init__(self, data: np.ndarray):
        self._value = np.asarray(data, dtype=np.int64)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get("out", ())
        for x in inputs + tuple(out):
            if not isinstance(
                x, self._HANDLED_TYPES + (type(self),)
            ):
                return NotImplemented
        inputs = tuple(
            x.value if isinstance(x, type(self)) else x for x in inputs
        )
        if out:
            kwargs["out"] = tuple(
                x.value if isinstance(x, type(self)) else x for x in out
            )
        result = getattr(ufunc, method)(*inputs, **kwargs)
        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        if method == "at":
            return None
        return type(self)(result)


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
