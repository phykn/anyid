# imstr

Compact serialization of NumPy uint8 arrays via WebP lossless compression + base64 encoding.

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
