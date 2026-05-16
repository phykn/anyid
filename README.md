# imstr

Compact serialization of NumPy uint8 arrays via WebP lossless compression + base64 encoding.

`imstr` converts 2D grayscale and 3D RGB/RGBA `uint8` arrays into plain strings
that can be stored or sent through text-only formats, then restores them without
loss.

## Installation

```bash
pip install imstr
```

## Usage

```python
import numpy as np
from imstr import encode, decode

arr = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
encoded = encode(arr)
decoded = decode(encoded)

assert np.array_equal(arr, decoded)
```

## Supported Arrays

- dtype: `np.uint8`
- shape: `(height, width)` grayscale, `(height, width, 3)` RGB, or
  `(height, width, 4)` RGBA

## Development

```bash
pip install -e ".[test]"
pytest
```
