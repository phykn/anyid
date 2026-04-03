import base64
import io
import numpy as np

from PIL import Image


def to_str(arr: np.ndarray, *, method: int = 0, quality: int = 0) -> str:
    if arr.dtype != np.uint8:
        raise ValueError("only uint8 array is supported")

    try:
        prefix = b"L" if arr.ndim == 2 else b"C"

        b = io.BytesIO()
        Image.fromarray(arr).save(b, format="WebP", lossless=True, method=method, quality=quality)
        return base64.b64encode(prefix + b.getvalue()).decode("utf-8")
    except Exception as e:
        raise ValueError(f"err: {e}")


def to_arr(s: str) -> np.ndarray:
    try:
        data = base64.b64decode(s)
        prefix, webp_data = data[:1], data[1:]

        b = io.BytesIO(webp_data)
        out = np.array(Image.open(b))

        if prefix == b"L" and out.ndim == 3:
            return out[:, :, 0]
        return out
    except Exception as e:
        raise ValueError(f"err: {e}")
