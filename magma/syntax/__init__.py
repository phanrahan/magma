from magma.syntax.combinational import combinational
try:
    import kratos
    from magma.syntax.verilog import build_kratos_debug_info
except ImportError:
    pass
