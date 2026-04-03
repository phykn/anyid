import hashlib
import numpy as np


def of_arr(arr: np.ndarray, *, prefix: str = "", length: int = 8) -> str:
    a = np.ascontiguousarray(arr)
    h = hashlib.md5()
    h.update(a.dtype.str.encode("ascii"))
    h.update(np.asarray(a.shape, dtype=np.int64).tobytes())
    h.update(memoryview(a))
    return prefix + h.hexdigest()[:length]


def of_str(s: str, *, prefix: str = "", length: int = 8) -> str:
    h = hashlib.md5(s.encode("utf-8"))
    return prefix + h.hexdigest()[:length]
