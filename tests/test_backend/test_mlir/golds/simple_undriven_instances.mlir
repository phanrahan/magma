module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_comb(%a: i16, %b: i16, %c: i16) -> (y: i16, z: i16) {
        %1 = hw.constant -1 : i16
        %0 = comb.xor %1, %a : i16
        %2 = comb.or %a, %0 : i16
        %3 = comb.or %2, %b : i16
        hw.output %3, %3 : i16, i16
    }
    hw.module @simple_undriven_instances() -> () {
        %1 = sv.wire sym @simple_undriven_instances.undriven_inst0 : !hw.inout<i16>
        %0 = sv.read_inout %1 : !hw.inout<i16>
        %3 = sv.wire sym @simple_undriven_instances.undriven_inst1 : !hw.inout<i16>
        %2 = sv.read_inout %3 : !hw.inout<i16>
        %5 = sv.wire sym @simple_undriven_instances.undriven_inst2 : !hw.inout<i16>
        %4 = sv.read_inout %5 : !hw.inout<i16>
        %6, %7 = hw.instance "simple_comb_inst0" @simple_comb(a: %0: i16, b: %2: i16, c: %4: i16) -> (y: i16, z: i16)
        %9 = sv.wire sym @simple_undriven_instances.undriven_inst3 : !hw.inout<i16>
        %8 = sv.read_inout %9 : !hw.inout<i16>
        %11 = sv.wire sym @simple_undriven_instances.undriven_inst4 : !hw.inout<i16>
        %10 = sv.read_inout %11 : !hw.inout<i16>
        %13 = sv.wire sym @simple_undriven_instances.undriven_inst5 : !hw.inout<i16>
        %12 = sv.read_inout %13 : !hw.inout<i16>
        %14, %15 = hw.instance "simple_comb_inst1" @simple_comb(a: %8: i16, b: %10: i16, c: %12: i16) -> (y: i16, z: i16)
    }
}
