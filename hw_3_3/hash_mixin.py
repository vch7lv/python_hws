import numpy as np


class HashMixin:

    def __hash__(self) -> int:
        arr = getattr(self, "_data", None)
        if arr is None:
            arr = getattr(self, "_value", None)
        arr = np.asarray(arr)
        s = int(arr.sum())
        rows, cols = arr.shape[0], arr.shape[1]
        return (s * 31 + rows * 31**2 + cols) % (2**32)
