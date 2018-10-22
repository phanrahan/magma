#  A circuit is a definition if it has instances
def isdefinition(circuit):
    'Return whether a circuit is a module definition'
    return getattr(circuit, "is_definition", False)
