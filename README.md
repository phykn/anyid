# imstr

Compact serialization of NumPy uint8 arrays via WebP lossless compression + base64 encoding.

## Features

- **Compact**: WebP lossless compression for efficient string representation.
- **Lossless**: 100% lossless reconstruction of pixel values and array shapes.
- **Fast**: Optimized for speed with configurable compression settings.

## Installation

```bash
pip install imstr
```

## Usage

```python
import numpy as np
from imstr import encode, decode

# Create a uint8 array
arr = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)

# Encode to a compact string
encoded = encode(arr)

# Decode back to a NumPy array
decoded = decode(encoded)

assert np.array_equal(arr, decoded)
```

## Development

Run tests:
```bash
pytest
```
