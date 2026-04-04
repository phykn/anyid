import hashlib
import numpy as np


def of_arr(arr: np.ndarray, *, prefix: str = "", length: int = 8) -> str:
    if not isinstance(arr, np.ndarray):
        raise ValueError("arr must be a numpy.ndarray")

    contiguous_arr = np.ascontiguousarray(arr)
    hasher = hashlib.md5()
    hasher.update(contiguous_arr.dtype.str.encode("ascii"))
    hasher.update(np.asarray(contiguous_arr.shape, dtype=np.int64).tobytes())
    hasher.update(memoryview(contiguous_arr))
    return prefix + hasher.hexdigest()[:length]


def of_str(text: str, *, prefix: str = "", length: int = 8) -> str:
    if not isinstance(text, str):
        raise ValueError("text must be a string")

    hasher = hashlib.md5(text.encode("utf-8"))
    return prefix + hasher.hexdigest()[:length]
