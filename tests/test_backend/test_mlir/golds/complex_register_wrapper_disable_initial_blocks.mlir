module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @complex_register_wrapper(%a: !hw.struct<x: i8, y: i1>, %b: !hw.array<6xi16>, %CLK: i1, %CE: i1, %ASYNCRESET: i1) -> (y: !hw.struct<u: !hw.struct<x: i8, y: i1>, v: !hw.array<6xi16>>) {
        %1 = sv.reg {name = "Register_inst0"} : !hw.inout<!hw.struct<x: i8, y: i1>>
        sv.alwaysff(posedge %CLK) {
            sv.if %CE {
                sv.passign %1, %a : !hw.struct<x: i8, y: i1>
            }
        } (asyncreset : posedge %ASYNCRESET) {
            sv.passign %1, %2 : !hw.struct<x: i8, y: i1>
        }
        %3 = hw.constant 10 : i8
        %4 = hw.constant 1 : i1
        %2 = hw.struct_create (%3, %4) : !hw.struct<x: i8, y: i1>
        %0 = sv.read_inout %1 : !hw.inout<!hw.struct<x: i8, y: i1>>
        %6 = sv.reg {name = "Register_inst1"} : !hw.inout<!hw.array<6xi16>>
        sv.alwaysff(posedge %CLK) {
            sv.passign %6, %b : !hw.array<6xi16>
        }
        %8 = hw.constant 0 : i16
        %9 = hw.constant 2 : i16
        %10 = hw.constant 4 : i16
        %11 = hw.constant 6 : i16
        %12 = hw.constant 8 : i16
        %13 = hw.constant 10 : i16
        %7 = hw.array_create %8, %9, %10, %11, %12, %13 : i16
        %5 = sv.read_inout %6 : !hw.inout<!hw.array<6xi16>>
        %14 = hw.struct_create (%0, %5) : !hw.struct<u: !hw.struct<x: i8, y: i1>, v: !hw.array<6xi16>>
        %15 = hw.struct_extract %a["x"] : !hw.struct<x: i8, y: i1>
        %17 = sv.reg {name = "Register_inst2"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %CE {
                sv.passign %17, %15 : i8
            }
        }
        %18 = hw.constant 0 : i8
        %16 = sv.read_inout %17 : !hw.inout<i8>
        hw.output %14 : !hw.struct<u: !hw.struct<x: i8, y: i1>, v: !hw.array<6xi16>>
    }
}
