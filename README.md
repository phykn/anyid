# AnyID

Fast, unique, and serializable identifiers for NumPy arrays.

## Features

- **Stable Deterministic Hash**: Generate consistent IDs from NumPy arrays based on data, shape, and dtype.
- **Optimized Serialization**: Efficient string representation using WebP Lossless compression and Base85 encoding (optimized for `uint8` image arrays).
- **Zero Loss**: 100% lossless reconstruction of pixel values and array shapes.

## Installation

```bash
pip install .
```

## Usage

### Generating IDs

```python
import numpy as np
from anyid.id import of_arr

arr = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
id_str = of_arr(arr)
print(id_str) # e.g., 'a1b2c3d4'
```

### Serialization

```python
from anyid.serialize import to_str, to_arr

# Serialize to a compact string
encoded = to_str(arr)

# Deserialize back to a NumPy array
arr_back = to_arr(encoded)

assert np.array_equal(arr, arr_back)
```

## Development

Run tests:
```bash
pytest
```