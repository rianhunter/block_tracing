# block_tracing

block_tracing is a tiny Python library that can be used to prevent
debuggers and other applications from inspecting the memory within
your process.

This is important for applications that store sensitive material
in memory, like keys.

# How to Use

Just call a function at the start of execution of your script.

```python
from block_tracing import block_tracing

try:
    block_tracing()
except (NotImplementedError, OSError):
    # handle failures
    pass
```

# Contact

Rian Hunter [@cejetvole](https://twitter.com/cejetvole)
