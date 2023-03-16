module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @aggregate_mux_wrapper(%a: !hw.struct<x: i8, y: i1>, %s: i1) -> (y: !hw.struct<x: i8, y: i1>) {
        %0 = hw.struct_extract %a["x"] : !hw.struct<x: i8, y: i1>
        %2 = hw.constant -1 : i8
        %1 = comb.xor %2, %0 : i8
        %3 = hw.struct_extract %a["y"] : !hw.struct<x: i8, y: i1>
        %5 = hw.constant -1 : i1
        %4 = comb.xor %5, %3 : i1
        %6 = hw.struct_create (%1, %4) : !hw.struct<x: i8, y: i1>
        %8 = sv.reg : !hw.inout<!hw.struct<x: i8, y: i1>>
        %7 = sv.read_inout %8 : !hw.inout<!hw.struct<x: i8, y: i1>>
        sv.alwayscomb {
            %10 = hw.constant 0 : i1
            %9 = comb.icmp eq %s, %10 : i1
            sv.if %9 {
                sv.bpassign %8, %6 : !hw.struct<x: i8, y: i1>
            } else {
                %12 = hw.constant 1 : i1
                %11 = comb.icmp eq %s, %12 : i1
                sv.if %11 {
                    sv.bpassign %8, %a : !hw.struct<x: i8, y: i1>
                } else {
                }
            }
        }
        hw.output %7 : !hw.struct<x: i8, y: i1>
    }
}
