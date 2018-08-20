# Logging
* `MAGMA_LOG_LEVEL`  
  Valid Inputs - DEBUG, WARN, ERROR  
  Currently these refer to the Python standard library logging levels,
  documented
  [here](https://docs.python.org/3/library/logging.html#logging-levels)

* `MAGMA_LOG_STREAM`  
  Valid Inputs - stdout, stderr  
  These refer to `sys.stdout` and `sys.stderr`, by default magma uses
  `sys.stderr`.

* `MAGMA_COREIR_BACKEND_LOG_LEVEL`  
  Same inputs as `MAGMA_LOG_LEVEL`. Sets the logging level specifically for the
  coreir backend.


Example
```
$ MAGMA_LOG_LEVEL=DEBUG MAGMA_COREIR_BACKEND_LOG_LEVEL=WARN MAGMA_LOG_STREAM=stdout pytest
```
