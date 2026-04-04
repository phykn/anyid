import numpy as np
import pytest

from anyid.id import of_arr, of_str


def test_of_arr_is_deterministic():
    arr = np.arange(12, dtype=np.uint8).reshape(3, 4)
    assert of_arr(arr) == of_arr(arr.copy())


def test_of_arr_changes_when_dtype_or_shape_changes():
    arr = np.arange(12, dtype=np.uint8).reshape(3, 4)
    arr_i16 = arr.astype(np.int16)
    arr_reshaped = arr.reshape(2, 6)

    assert of_arr(arr) != of_arr(arr_i16)
    assert of_arr(arr) != of_arr(arr_reshaped)


def test_of_str_is_deterministic():
    assert of_str("abc") == of_str("abc")


def test_length_is_not_restricted():
    arr = np.zeros((2, 2), dtype=np.uint8)
    assert of_arr(arr, length=0) == ""
    assert len(of_arr(arr, length=999)) == 32
    assert of_str("abc", length=0) == ""
    assert len(of_str("abc", length=999)) == 32


def test_invalid_input_type_fails():
    with pytest.raises(ValueError, match="arr must be a numpy.ndarray"):
        of_arr([[1, 2], [3, 4]])  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="text must be a string"):
        of_str(123)  # type: ignore[arg-type]
