hw.module @complex_compile_guard2(%I_x: i8, %O_y: i1, %CLK: i1) -> (I_y: i1, O_x: i8) {
    %0 = comb.extract %I_x from 4 : (i8) -> i1
    %1 = comb.extract %I_x from 5 : (i8) -> i1
    %2 = comb.extract %I_x from 6 : (i8) -> i1
    %3 = comb.extract %I_x from 7 : (i8) -> i1
    %4 = comb.extract %I_x from 0 : (i8) -> i1
    %5 = comb.extract %I_x from 1 : (i8) -> i1
    %6 = comb.extract %I_x from 2 : (i8) -> i1
    %7 = comb.extract %I_x from 3 : (i8) -> i1
    %8 = comb.concat %7, %6, %5, %4, %3, %2, %1, %0 : i1, i1, i1, i1, i1, i1, i1, i1
    sv.ifdef "COND1" {
        %10 = sv.reg {name = "Register_inst0"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %10, %8 : i8
        }
        sv.initial {
            sv.bpassign %10, %11 : i8
        }
        %9 = sv.read_inout %10 : !hw.inout<i8>
        %12 = comb.extract %9 from 5 : (i8) -> i1
        %13 = comb.extract %9 from 6 : (i8) -> i1
        %14 = comb.concat %13, %12 : i1, i1
        sv.ifdef "COND2" {
        } else {
            %16 = sv.reg {name = "Register_inst1"} : !hw.inout<i2>
            sv.alwaysff(posedge %CLK) {
                sv.passign %16, %14 : i2
            }
            sv.initial {
                sv.bpassign %16, %17 : i2
            }
            %15 = sv.read_inout %16 : !hw.inout<i2>
        }
        %18 = comb.extract %9 from 2 : (i8) -> i1
        %19 = comb.extract %9 from 3 : (i8) -> i1
        %20 = comb.extract %9 from 4 : (i8) -> i1
        %21 = comb.extract %9 from 7 : (i8) -> i1
        %22 = comb.concat %21, %13, %12, %20, %19, %18 : i1, i1, i1, i1, i1, i1
        sv.ifdef "COND3" {
        } else {
            %24 = sv.reg {name = "Register_inst2"} : !hw.inout<i6>
            sv.alwaysff(posedge %CLK) {
                sv.passign %24, %22 : i6
            }
            sv.initial {
                sv.bpassign %24, %25 : i6
            }
            %23 = sv.read_inout %24 : !hw.inout<i6>
        }
        %26 = comb.extract %9 from 0 : (i8) -> i1
        %28 = sv.reg {name = "Register_inst3"} : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %28, %26 : i1
        }
        sv.initial {
            sv.bpassign %28, %29 : i1
        }
        %27 = sv.read_inout %28 : !hw.inout<i1>
    }
    %11 = hw.constant 0 : i8
    %17 = hw.constant 0 : i2
    %25 = hw.constant 0 : i6
    %29 = hw.constant 0 : i1
    hw.output %O_y, %I_x : i1, i8
}
