import libcst


files = [
    "riscv_mini/tile.py",
    "riscv_mini/nasti.py",
    "riscv_mini/br_cond.py",
    "riscv_mini/imm_gen.py",
    "riscv_mini/alu.py",
    "riscv_mini/instructions.py",
    "riscv_mini/control.py",
    "riscv_mini/cache.py",
    "riscv_mini/__init__.py",
    "riscv_mini/core.py",
    "riscv_mini/csr_gen.py",
    "riscv_mini/csr.py",
    "riscv_mini/reg_file.py",
    "riscv_mini/main.py",
    "riscv_mini/data_path.py",
    "riscv_mini/const.py"
]

for file in files:
    with open(file, "r") as f:
        cst = libcst.parse_module(f.read())
    with open(f"temp/{file}", "w") as f:
        f.write(cst.code)
