import base64
import io
import numpy as np

from PIL import Image


def encode(arr: np.ndarray, *, method: int = 0, quality: int = 0) -> str:
    if arr.dtype != np.uint8:
        raise ValueError("only uint8 array is supported")
    if arr.ndim == 2:
        prefix = b"L"
    elif arr.ndim == 3 and arr.shape[2] in (3, 4):
        prefix = b"C"
    else:
        raise ValueError("array must be 2D grayscale or 3D RGB/RGBA")

    try:
        buffer = io.BytesIO()
        Image.fromarray(arr).save(
            buffer,
            format="WebP",
            lossless=True,
            method=method,
            quality=quality,
        )
        return base64.b64encode(prefix + buffer.getvalue()).decode("utf-8")

    except Exception as exc:
        raise ValueError(f"failed to serialize array: {exc}") from exc


def decode(encoded_str: str) -> np.ndarray:
    try:
        payload = base64.b64decode(encoded_str, validate=True)
        if len(payload) < 2:
            raise ValueError("payload is too short")

        prefix, webp_data = payload[:1], payload[1:]
        if prefix not in (b"L", b"C"):
            raise ValueError("invalid payload prefix")

        buffer = io.BytesIO(webp_data)
        with Image.open(buffer) as image:
            decoded_array = np.array(image)

        if prefix == b"L" and decoded_array.ndim == 3:
            return decoded_array[:, :, 0]
        return decoded_array

    except Exception as exc:
        raise ValueError(f"failed to deserialize array: {exc}") from exc
