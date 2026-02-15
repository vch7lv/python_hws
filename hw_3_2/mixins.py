import numpy as np
import numbers


def _matrix_format(arr: np.ndarray) -> str:
    return "\n".join(" ".join(str(int(x)) for x in row) for row in arr)


class StrMixin:

    def __str__(self) -> str:
        val = getattr(self, "value", None)
        if val is None:
            val = getattr(self, "_value", None)
        if val is not None:
            return _matrix_format(np.asarray(val))
        return super().__str__()


class FileWriterMixin:

    def to_file(self, path: str) -> None:
        with open(path, "w") as f:
            f.write(str(self))
            f.write("\n")


class GetterSetterMixin:

    @property
    def value(self) -> np.ndarray:
        return getattr(self, "_value")

    @value.setter
    def value(self, data: np.ndarray) -> None:
        object.__setattr__(self, "_value", np.asarray(data, dtype=np.int64))
