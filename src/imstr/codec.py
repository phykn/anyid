import base64
import io
import numpy as np

from PIL import Image


def encode(arr: np.ndarray, *, method: int = 0, quality: int = 0) -> str:
    """Serialize a uint8 NumPy array to a base64 string via WebP-lossless.

    Accepts 2D grayscale or 3D RGB/RGBA arrays. The payload is prefixed with
    a 1-byte tag (``b"L"`` for grayscale, ``b"C"`` for color) before base64
    encoding so :func:`decode` can restore the original shape. ``method`` and
    ``quality`` are passed through to Pillow's WebP encoder; the defaults
    (both ``0``) favour fastest encoding.

    Raises:
        ValueError: with message starting ``"only uint8 array is supported"``
            if ``arr.dtype`` is not ``uint8``; ``"array must be 2D grayscale
            or 3D RGB/RGBA"`` if the shape is unsupported; or ``"failed to
            serialize array"`` if the underlying WebP encode fails.
    """
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
    """Deserialize a base64 string produced by :func:`encode` back to a uint8 array.

    Reads the 1-byte ``b"L"``/``b"C"`` prefix to decide whether to return a
    2D grayscale or 3D RGB/RGBA array.

    Raises:
        ValueError: with message starting ``"invalid payload prefix"`` if the
            leading byte is neither ``b"L"`` nor ``b"C"``, or ``"failed to
            deserialize array"`` if base64 decoding or WebP decoding fails.
    """
    try:
        payload = base64.b64decode(encoded_str, validate=True)
        prefix, webp_data = payload[:1], payload[1:]
        if prefix not in (b"L", b"C"):
            raise ValueError("invalid payload prefix")

        buffer = io.BytesIO(webp_data)
        with Image.open(buffer) as image:
            decoded_array = np.array(image)

        # PIL re-decodes single-channel WebP as RGB; restore the original 2D shape.
        if prefix == b"L" and decoded_array.ndim == 3:
            return decoded_array[:, :, 0]
        return decoded_array

    except Exception as exc:
        raise ValueError(f"failed to deserialize array: {exc}") from exc
