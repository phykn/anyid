import base64
import numpy as np
import pytest
from anyid.serialize import to_str, to_arr


def test_lossless_random():
    # Test random 256x256 uint8 RGB
    arr = np.random.randint(0, 256, (256, 256, 3), dtype=np.uint8)
    s = to_str(arr)
    arr_back = to_arr(s)

    assert np.array_equal(arr, arr_back)
    assert arr.dtype == arr_back.dtype
    assert arr.shape == arr_back.shape


def test_lossless_grayscale():
    # Test random 100x100 uint8 Grayscale
    arr = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
    s = to_str(arr)
    arr_back = to_arr(s)

    assert np.array_equal(arr, arr_back)
    assert arr.dtype == arr_back.dtype
    assert arr.shape == arr_back.shape


def test_other_dtype_fails():
    # Test that float32 fails as expected
    arr = np.random.rand(10, 10).astype(np.float32)
    with pytest.raises(ValueError, match="only uint8 array is supported"):
        to_str(arr)


def test_efficiency():
    # Gradient should result in a very short string compared to raw
    grad = np.tile(np.linspace(0, 255, 256, dtype=np.uint8), (256, 1))
    s = to_str(grad)
    # 256*256*1 bytes = 65,536 bytes. Base64 should be around ~87,000+ chars if uncompressed.
    # But WebP Lossless for gradient should be very small.
    assert len(s) < 1000  # Expect highly efficient compression


def test_invalid_base64_fails():
    with pytest.raises(ValueError, match="failed to deserialize array"):
        to_arr("not-base64")


def test_invalid_prefix_fails():
    payload = b"X" + b"abc"
    s = base64.b64encode(payload).decode("utf-8")
    with pytest.raises(ValueError, match="invalid payload prefix"):
        to_arr(s)


def test_invalid_webp_payload_fails():
    payload = b"C" + b"not-webp"
    s = base64.b64encode(payload).decode("utf-8")
    with pytest.raises(ValueError, match="failed to deserialize array"):
        to_arr(s)


def test_invalid_ndim_fails():
    arr = np.random.randint(0, 256, (2, 3, 4, 5), dtype=np.uint8)
    with pytest.raises(ValueError, match="array must be 2D grayscale or 3D RGB/RGBA"):
        to_str(arr)


def test_invalid_channel_count_fails():
    arr = np.random.randint(0, 256, (10, 10, 2), dtype=np.uint8)
    with pytest.raises(ValueError, match="array must be 2D grayscale or 3D RGB/RGBA"):
        to_str(arr)
