import magma as m


from riscv_mini.tile import Tile


m.compile("build/Tile", Tile(32), disable_ndarray=True)
