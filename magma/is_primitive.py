def isprimitive(circuit):
    return getattr(circuit, "primitive", False)
