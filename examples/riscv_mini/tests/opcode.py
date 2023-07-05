from hwtypes import BitVector as BV


class Opcode:
    # Special immediate instructions
    LUI = BV[7](0b0110111)
    AUIPC = BV[7](0b0010111)

    # Jump instructions
    JAL = BV[7](0b1101111)
    JALR = BV[7](0b1100111)

    # Branch instructions
    BRANCH = BV[7](0b1100011)

    # Load and store instrucdtions
    STORE = BV[7](0b0100011)
    LOAD = BV[7](0b0000011)

    # Arithmetic instructions
    RTYPE = BV[7](0b0110011)
    ITYPE = BV[7](0b0010011)

    MEMORY = BV[7](0b0001111)
    SYSTEM = BV[7](0b1110011)


class Funct3:
    # Branch function codes
    BEQ = BV[3](0b000)
    BNE = BV[3](0b001)
    BLT = BV[3](0b100)
    BGE = BV[3](0b101)
    BLTU = BV[3](0b110)
    BGEU = BV[3](0b111)

    # Load and store function codes
    LB = BV[3](0b000)
    LH = BV[3](0b001)
    LW = BV[3](0b010)
    LBU = BV[3](0b100)
    LHU = BV[3](0b101)
    SB = BV[3](0b000)
    SH = BV[3](0b001)
    SW = BV[3](0b010)

    # Arithmetic R-type and I-type functions codes
    ADD = BV[3](0b000)
    SLL = BV[3](0b001)
    SLT = BV[3](0b010)
    SLTU = BV[3](0b011)
    XOR = BV[3](0b100)
    OR = BV[3](0b110)
    AND = BV[3](0b111)
    SR = BV[3](0b101)

    CSRRW = BV[3](0b001)
    CSRRS = BV[3](0b010)
    CSRRC = BV[3](0b011)
    CSRRWI = BV[3](0b101)
    CSRRSI = BV[3](0b110)
    CSRRCI = BV[3](0b111)


class Funct7:
    U = BV[7](0b0000000)
    S = BV[7](0b0100000)


class Funct12:
    ECAL = BV[12](0b000000000000)
    EBREAK = BV[12](0b000000000001)
    ERET = BV[12](0b000100000000)
