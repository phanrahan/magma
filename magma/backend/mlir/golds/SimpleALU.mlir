hw.module @SimpleALU(%a: i4, %b: i4, %opcode: i2) -> (out: i4) {
    %0 = hw.constant 2 : i2
    %1 = comb.icmp eq %opcode, %0 : i2
    %3 = hw.array_create %b, %a : i4
    %2 = hw.array_get %3[%1] : !hw.array<2xi4>
    %4 = comb.sub %a, %b : i4
    %5 = hw.constant 1 : i2
    %6 = comb.icmp eq %opcode, %5 : i2
    %8 = hw.array_create %2, %4 : i4
    %7 = hw.array_get %8[%6] : !hw.array<2xi4>
    %9 = comb.add %a, %b : i4
    %10 = hw.constant 0 : i2
    %11 = comb.icmp eq %opcode, %10 : i2
    %13 = hw.array_create %7, %9 : i4
    %12 = hw.array_get %13[%11] : !hw.array<2xi4>
    hw.output %12 : i4
}
