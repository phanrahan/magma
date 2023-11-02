module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @complex_wire(in %I0: i8, in %I1: i1, in %I2: !hw.array<4xi8>, out O0: i8, out O1: i1, out O2: !hw.array<4xi8>) {
        %1 = sv.wire sym @complex_wire.tmp0 name "tmp0" : !hw.inout<i8>
        sv.assign %1, %I0 : i8
        %0 = sv.read_inout %1 : !hw.inout<i8>
        %3 = sv.wire sym @complex_wire.tmp1 name "tmp1" : !hw.inout<i1>
        sv.assign %3, %I1 : i1
        %2 = sv.read_inout %3 : !hw.inout<i1>
        %5 = sv.wire sym @complex_wire.tmp2 name "tmp2" : !hw.inout<!hw.array<4xi8>>
        sv.assign %5, %I2 : !hw.array<4xi8>
        %4 = sv.read_inout %5 : !hw.inout<!hw.array<4xi8>>
        hw.output %0, %2, %4 : i8, i1, !hw.array<4xi8>
    }
}
