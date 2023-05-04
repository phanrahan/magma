module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_tuple_bulk_resolve_False(%I: !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>, %S: i2, %CLK: i1) -> (O: !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %3 = sv.reg name "y" : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        sv.alwaysff(posedge %CLK) {
            sv.passign %3, %1 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        }
        %5 = hw.constant 0 : i8
        %8 = hw.constant 0 : i8
        %9 = hw.constant 0 : i8
        %7 = hw.struct_create (%8, %9) : !hw.struct<x: i8, y: i8>
        %11 = hw.constant 0 : i8
        %12 = hw.constant 0 : i8
        %10 = hw.struct_create (%11, %12) : !hw.struct<x: i8, y: i8>
        %6 = hw.struct_create (%7, %10) : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %4 = hw.struct_create (%5, %6) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        sv.initial {
            sv.bpassign %3, %4 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        }
        %2 = sv.read_inout %3 : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        %13 = comb.extract %S from 1 : (i2) -> i1
        %14 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %15 = hw.struct_extract %I["y"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %18 = sv.reg : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        %17 = sv.read_inout %18 : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        %19 = sv.reg : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        %1 = sv.read_inout %19 : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        sv.alwayscomb {
            sv.if %0 {
                %24 = hw.struct_create (%20, %21) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                sv.bpassign %18, %24 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                %25 = hw.struct_create (%22, %23) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                sv.bpassign %19, %25 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
            } else {
                %26 = hw.struct_create (%20, %21) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                sv.bpassign %19, %26 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                sv.if %13 {
                    %27 = hw.struct_create (%14, %15) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                    sv.bpassign %18, %27 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                } else {
                    %28 = hw.struct_create (%20, %21) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                    sv.bpassign %18, %28 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                }
            }
        }
        %20 = hw.struct_extract %16["x"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %21 = hw.struct_extract %16["y"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %22 = hw.struct_extract %2["x"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %23 = hw.struct_extract %2["y"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %29 = sv.reg name "x" : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        sv.alwaysff(posedge %CLK) {
            sv.passign %29, %17 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        }
        sv.initial {
            sv.bpassign %29, %4 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        }
        %16 = sv.read_inout %29 : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        hw.output %16 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
    }
}
