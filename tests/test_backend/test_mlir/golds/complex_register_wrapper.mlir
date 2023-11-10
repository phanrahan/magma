module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @complex_register_wrapper(in %a: !hw.struct<x: i8, y: i1>, in %b: !hw.array<6xi16>, in %CLK: i1, in %CE: i1, in %ASYNCRESET: i1, out y: !hw.struct<u: !hw.struct<x: i8, y: i1>, v: !hw.array<6xi16>>) {
        %1 = sv.reg name "Register_inst0" : !hw.inout<!hw.struct<x: i8, y: i1>>
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
        sv.initial {
            sv.bpassign %1, %2 : !hw.struct<x: i8, y: i1>
        }
        %0 = sv.read_inout %1 : !hw.inout<!hw.struct<x: i8, y: i1>>
        %6 = sv.reg name "Register_inst1" : !hw.inout<!hw.array<6xi16>>
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
        sv.initial {
            sv.bpassign %6, %7 : !hw.array<6xi16>
        }
        %5 = sv.read_inout %6 : !hw.inout<!hw.array<6xi16>>
        %14 = hw.struct_create (%0, %5) : !hw.struct<u: !hw.struct<x: i8, y: i1>, v: !hw.array<6xi16>>
        %15 = hw.struct_extract %a["x"] : !hw.struct<x: i8, y: i1>
        %17 = sv.reg name "Register_inst2" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %CE {
                sv.passign %17, %15 : i8
            }
        }
        %18 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %17, %18 : i8
        }
        %16 = sv.read_inout %17 : !hw.inout<i8>
        hw.output %14 : !hw.struct<u: !hw.struct<x: i8, y: i1>, v: !hw.array<6xi16>>
    }
}
