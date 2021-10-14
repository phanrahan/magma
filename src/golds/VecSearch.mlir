hw.module @Register(%I: i3, %CLK: i1) -> (%O: i3) {
    %1 = sv.reg {name = "reg_P3_inst0"} : !hw.inout<i3>
    sv.alwaysff(posedge %CLK) {
        sv.passign %1, %I : i3
    }
    %0 = sv.read_inout %1 : !hw.inout<i3>
    hw.output %0 : i3
}
hw.module @Mux7xUInt4(%I0: i4, %I1: i4, %I2: i4, %I3: i4, %I4: i4, %I5: i4, %I6: i4, %S: i3) -> (%O: i4) {
    %0 = hw.array_create %I6, %I5, %I4, %I3, %I2, %I1, %I0 : i4
    %1 = hw.struct_create (%0, %S) : !hw.struct<data: !hw.array<7xi4>, sel: i3>
    %3 = hw.struct_extract %1["data"] : !hw.struct<data: !hw.array<7xi4>, sel: i3>
    %4 = hw.struct_extract %1["sel"] : !hw.struct<data: !hw.array<7xi4>, sel: i3>
    %2 = hw.array_get %3[%4] : !hw.array<7xi4>
    hw.output %2 : i4
}
hw.module @VecSearch(%CLK: i1) -> (%out: i4) {
    %0 = hw.constant 0 : i4
    %1 = hw.constant 4 : i4
    %2 = hw.constant 15 : i4
    %3 = hw.constant 14 : i4
    %4 = hw.constant 2 : i4
    %5 = hw.constant 5 : i4
    %6 = hw.constant 13 : i4
    %7 = hw.constant 1 : i3
    %9 = comb.add %8, %7 : i3
    %8 = hw.instance "Register_inst0" @Register(%9, %CLK) : (i3, i1) -> (i3)
    %10 = hw.instance "Mux7xUInt4_inst0" @Mux7xUInt4(%0, %1, %2, %3, %4, %5, %6, %8) : (i4, i4, i4, i4, i4, i4, i4, i3) -> (i4)
    hw.output %10 : i4
}
