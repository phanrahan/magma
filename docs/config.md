# Configuring Magma

## Rewire Log Level
By default, magma logs rewiring (wiring an already driven value with a new
value) as a warning. You can change this level to one of: `"DEBUG", "INFO",
"ERROR"` using the environment variable `MAGMA_REWIRE_LOG_LEVEL`, or by using
the magma config interface.
```python
from magma.config import config
config.rewire_log_level = "ERROR"
```
