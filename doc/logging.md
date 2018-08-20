Basic example
```
$ MAGMA_LOG_LEVEL=DEBUG MAGMA_COREIR_BACKEND_LOG_LEVEL=WARN MAGMA_LOG_STREAM=stdout pytest
```

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

* `MAGMA_INCLUDE_WIRE_TRACEBACK`  
  Setting this variable enables the traceback feature of magma's error
  reporting. When certain wiring errors are made, magma will dump a traceback
  similar to the message seen from Python Exceptions, which can be useful for
  debugging complex wiring errors with multiple levels of indirection (calls to
  multiple generators).
 

* `MAGMA_ERROR_TRACEBACK_LIMIT`  
  Valid Inputs - Positive integers (default: 5)
  Set the maximum number of stack frames printed in the traceback for magma
  errors (e.g. wiring). Here's an example with the default level of 5.
  ```
    ERROR:magma:==================== BEGIN: MAGMA ERROR ====================
    ERROR:magma:  File ".../miniconda3/lib/python3.6/site-packages/IPython/core/shellapp.py", line 321, in _e
    xec_file
    ERROR:magma:    raise_exceptions=True)
    ERROR:magma:  File ".../miniconda3/lib/python3.6/site-packages/IPython/core/interactiveshell.py", line 24
    63, in safe_execfile
    ERROR:magma:    self.compile if shell_futures else None)
    ERROR:magma:  File ".../miniconda3/lib/python3.6/site-packages/IPython/utils/py3compat.py", line 186, in
    execfile
    ERROR:magma:    exec(compiler(f.read(), fname, 'exec'), glob, loc)
    ERROR:magma:  File ".../magma/tests/test_wire/test_errors.py", line 27, in <module>
    ERROR:magma:    test_output_as_input(None)
    ERROR:magma:  File ".../magma/tests/test_wire/test_errors.py", line 21, in test_output
    _as_input
    ERROR:magma:    wire(main.I, a.O)
    ERROR:magma:WIRING ERROR: Using an output as an input inst0.O
    ERROR:magma:==================== END: MAGMA ERROR ====================
  ```

  Here's an example setting it to another level
  ```
    ❯ MAGMA_ERROR_TRACEBACK_LIMIT=10 python tests/test_wire/test_errors.py
    ERROR:magma:==================== BEGIN: MAGMA ERROR ====================
    ERROR:magma:  File "<decorator-gen-112>", line 2, in initialize
    ERROR:magma:  File ".../miniconda3/lib/python3.6/site-packages/traitlets/config/application.py", line 87,
     in catch_config_error
    ERROR:magma:    return method(app, *args, **kwargs)
    ERROR:magma:  File ".../miniconda3/lib/python3.6/site-packages/IPython/terminal/ipapp.py", line 323, in i
    nitialize
    ERROR:magma:    self.init_code()
    ERROR:magma:  File ".../miniconda3/lib/python3.6/site-packages/IPython/core/shellapp.py", line 269, in in
    it_code
    ERROR:magma:    self._run_cmd_line_code()
    ERROR:magma:  File ".../miniconda3/lib/python3.6/site-packages/IPython/core/shellapp.py", line 387, in _r
    un_cmd_line_code
    ERROR:magma:    self._exec_file(fname, shell_futures=True)
    ERROR:magma:  File ".../miniconda3/lib/python3.6/site-packages/IPython/core/shellapp.py", line 321, in _e
    xec_file
    ERROR:magma:    raise_exceptions=True)
    ERROR:magma:  File ".../miniconda3/lib/python3.6/site-packages/IPython/core/interactiveshell.py", line 24
    63, in safe_execfile
    ERROR:magma:    self.compile if shell_futures else None)
    ERROR:magma:  File ".../miniconda3/lib/python3.6/site-packages/IPython/utils/py3compat.py", line 186, in
    execfile
    ERROR:magma:    exec(compiler(f.read(), fname, 'exec'), glob, loc)
    ERROR:magma:  File ".../magma/tests/test_wire/test_errors.py", line 27, in <module>
    ERROR:magma:    test_output_as_input(None)
    ERROR:magma:  File ".../magma/tests/test_wire/test_errors.py", line 21, in test_output
    _as_input
    ERROR:magma:    wire(main.I, a.O)
    ERROR:magma:WIRING ERROR: Using an output as an input inst0.O
    ERROR:magma:==================== END: MAGMA ERROR ====================
  ```
