module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_spurious_assign_False(%x: i8, %y: i1, %z: i2, %CLK: i1) -> (O: !hw.struct<x: i8, y: !hw.struct<x: i8, y: i1>>) {
        %0 = comb.extract %z from 0 : (i2) -> i1
        %1 = comb.extract %z from 1 : (i2) -> i1
        %2 = hw.constant 1 : i1
        %3 = hw.constant 1 : i8
        %5 = hw.constant -1 : i8
        %4 = comb.xor %5, %x : i8
        %8 = sv.reg : !hw.inout<i8>
        %6 = sv.read_inout %8 : !hw.inout<i8>
        %9 = sv.reg : !hw.inout<i1>
        %7 = sv.read_inout %9 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %0 {
                sv.if %1 {
                    sv.bpassign %8, %x : i8
                } else {
                    sv.bpassign %8, %3 : i8
                }
            } else {
                sv.bpassign %8, %4 : i8
            }
        }
        %10 = hw.constant 1 : i1
        %12 = hw.constant -1 : i1
        %11 = comb.xor %12, %y : i1
        %15 = sv.reg : !hw.inout<i1>
        %13 = sv.read_inout %15 : !hw.inout<i1>
        %16 = sv.reg : !hw.inout<i1>
        %14 = sv.read_inout %16 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %1 {
                sv.bpassign %15, %y : i1
            } else {
                sv.bpassign %15, %11 : i1
            }
        }
        %17 = hw.struct_create (%6, %13) : !hw.struct<x: i8, y: i1>
        %18 = hw.struct_create (%x, %17) : !hw.struct<x: i8, y: !hw.struct<x: i8, y: i1>>
        %20 = sv.reg name "Register_inst0" : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: i8, y: i1>>>
        sv.alwaysff(posedge %CLK) {
            sv.if %0 {
                sv.passign %20, %18 : !hw.struct<x: i8, y: !hw.struct<x: i8, y: i1>>
            }
        }
        %22 = hw.constant 0 : i8
        %24 = hw.constant 0 : i8
        %25 = hw.constant 0 : i1
        %23 = hw.struct_create (%24, %25) : !hw.struct<x: i8, y: i1>
        %21 = hw.struct_create (%22, %23) : !hw.struct<x: i8, y: !hw.struct<x: i8, y: i1>>
        sv.initial {
            sv.bpassign %20, %21 : !hw.struct<x: i8, y: !hw.struct<x: i8, y: i1>>
        }
        %19 = sv.read_inout %20 : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: i8, y: i1>>>
        hw.output %19 : !hw.struct<x: i8, y: !hw.struct<x: i8, y: i1>>
    }
}
