import base64
import numpy as np
import pytest
from imstr.codec import encode, decode


def test_lossless_random():
    arr = np.random.randint(0, 256, (256, 256, 3), dtype=np.uint8)
    s = encode(arr)
    arr_back = decode(s)

    assert np.array_equal(arr, arr_back)
    assert arr.dtype == arr_back.dtype
    assert arr.shape == arr_back.shape


def test_lossless_grayscale():
    arr = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
    s = encode(arr)
    arr_back = decode(s)

    assert np.array_equal(arr, arr_back)
    assert arr.dtype == arr_back.dtype
    assert arr.shape == arr_back.shape


def test_other_dtype_fails():
    arr = np.random.rand(10, 10).astype(np.float32)
    with pytest.raises(ValueError, match="only uint8 array is supported"):
        encode(arr)


def test_efficiency():
    # 65,536 raw bytes → ~87k base64 chars uncompressed; WebP lossless crushes
    # a gradient to well under 1k.
    grad = np.tile(np.linspace(0, 255, 256, dtype=np.uint8), (256, 1))
    s = encode(grad)
    assert len(s) < 1000


def test_invalid_base64_fails():
    with pytest.raises(ValueError, match="failed to deserialize array"):
        decode("not-base64")


def test_invalid_prefix_fails():
    payload = b"X" + b"abc"
    s = base64.b64encode(payload).decode("utf-8")
    with pytest.raises(ValueError, match="invalid payload prefix"):
        decode(s)


def test_invalid_webp_payload_fails():
    payload = b"C" + b"not-webp"
    s = base64.b64encode(payload).decode("utf-8")
    with pytest.raises(ValueError, match="failed to deserialize array"):
        decode(s)


def test_invalid_ndim_fails():
    arr = np.random.randint(0, 256, (2, 3, 4, 5), dtype=np.uint8)
    with pytest.raises(ValueError, match="array must be 2D grayscale or 3D RGB/RGBA"):
        encode(arr)


def test_invalid_channel_count_fails():
    arr = np.random.randint(0, 256, (10, 10, 2), dtype=np.uint8)
    with pytest.raises(ValueError, match="array must be 2D grayscale or 3D RGB/RGBA"):
        encode(arr)


def test_valid_prefix_empty_webp_fails():
    for prefix in (b"L", b"C"):
        s = base64.b64encode(prefix).decode("utf-8")
        with pytest.raises(ValueError, match="failed to deserialize array"):
            decode(s)
