hw.module @Register(%I: i3, %CLK: i1) -> (%O: i3) {
    %0 = sv.reg {name = "reg_P3_inst0"} : !hw.inout<i3>
    %1 = hw.constant 0 : i3
    %2 = sv.read_inout %0 : !hw.inout<i3>
    sv.alwaysff(posedge %CLK) { sv.passign %0, %I : i3 }
    sv.initial { sv.bpassign %0, %1 : i3 }
    hw.output %2 : i3
}
hw.module @Mux7xUInt4(%I0: i4, %I1: i4, %I2: i4, %I3: i4, %I4: i4, %I5: i4, %I6: i4, %S: i3) -> (%O: i4) {
    %0 = hw.array_create %I6, %I5, %I4, %I3, %I2, %I1, %I0 : i4
    %1 = hw.struct_create (%0, %S) : !hw.struct<data: !hw.array<7xi4>, sel: i3>
    %2 = hw.struct_extract %1["data"] : !hw.struct<data: !hw.array<7xi4>, sel: i3>
    %3 = hw.struct_extract %1["sel"] : !hw.struct<data: !hw.array<7xi4>, sel: i3>
    %4 = hw.array_get %2[%3] : !hw.array<7xi4>
    hw.output %4 : i4
}
hw.module @VecSearch(%CLK: i1) -> (%out: i4) {
    %0 = hw.constant 1 : i3
    %1 = hw.constant 0 : i4
    %2 = hw.constant 4 : i4
    %3 = hw.constant 15 : i4
    %4 = hw.constant 14 : i4
    %5 = hw.constant 2 : i4
    %6 = hw.constant 5 : i4
    %7 = hw.constant 13 : i4
    %8 = sv.wire : !hw.inout<i3>
    %9 = sv.read_inout %8 : !hw.inout<i3>
    %10 = comb.add %9, %0 : i3
    %11 = hw.instance "Register_inst0" @Register(%10, %CLK) : (i3, i1) -> (i3)
    %12 = hw.instance "Mux7xUInt4_inst0" @Mux7xUInt4(%1, %2, %3, %4, %5, %6, %7, %11) : (i4, i4, i4, i4, i4, i4, i4, i3) -> (i4)
    sv.assign %8, %11 : i3
    hw.output %12 : i4
}
