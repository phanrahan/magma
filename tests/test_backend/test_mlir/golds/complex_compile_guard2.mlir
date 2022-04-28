hw.module @complex_compile_guard2(%I_x: !hw.struct<a: i4, b: i4>, %O_y: i1, %CLK: i1) -> (I_y: i1, O_x: !hw.struct<a: i4, b: i4>) {
    %0 = hw.struct_extract %I_x["b"] : !hw.struct<a: i4, b: i4>
    %1 = hw.struct_extract %I_x["a"] : !hw.struct<a: i4, b: i4>
    %2 = hw.struct_create (%0, %1) : !hw.struct<a: i4, b: i4>
    sv.ifdef "COND1" {
        %4 = sv.reg {name = "Register_inst0"} : !hw.inout<!hw.struct<a: i4, b: i4>>
        sv.alwaysff(posedge %CLK) {
            sv.passign %4, %2 : !hw.struct<a: i4, b: i4>
        }
        sv.initial {
            sv.bpassign %4, %5 : !hw.struct<a: i4, b: i4>
        }
        %3 = sv.read_inout %4 : !hw.inout<!hw.struct<a: i4, b: i4>>
        %8 = hw.struct_extract %3["b"] : !hw.struct<a: i4, b: i4>
        %9 = hw.struct_extract %3["a"] : !hw.struct<a: i4, b: i4>
        %10 = hw.struct_create (%8, %9) : !hw.struct<a: i4, b: i4>
        sv.ifdef "COND2" {
        } else {
            %12 = sv.reg {name = "Register_inst1"} : !hw.inout<!hw.struct<a: i4, b: i4>>
            sv.alwaysff(posedge %CLK) {
                sv.passign %12, %10 : !hw.struct<a: i4, b: i4>
            }
            sv.initial {
                sv.bpassign %12, %5 : !hw.struct<a: i4, b: i4>
            }
            %11 = sv.read_inout %12 : !hw.inout<!hw.struct<a: i4, b: i4>>
        }
        %13 = comb.extract %9 from 1 : (i4) -> i1
        %14 = comb.extract %9 from 2 : (i4) -> i1
        %15 = comb.concat %14, %13 : i1, i1
        sv.ifdef "COND3" {
        } else {
            %17 = sv.reg {name = "Register_inst2"} : !hw.inout<i2>
            sv.alwaysff(posedge %CLK) {
                sv.passign %17, %15 : i2
            }
            sv.initial {
                sv.bpassign %17, %18 : i2
            }
            %16 = sv.read_inout %17 : !hw.inout<i2>
        }
    }
    %6 = hw.constant 0 : i4
    %7 = hw.constant 0 : i4
    %5 = hw.struct_create (%6, %7) : !hw.struct<a: i4, b: i4>
    %18 = hw.constant 0 : i2
    hw.output %O_y, %I_x : i1, !hw.struct<a: i4, b: i4>
}
