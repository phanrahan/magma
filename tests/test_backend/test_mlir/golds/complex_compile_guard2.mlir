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
        %12 = comb.extract %9 from 0 : (i8) -> i1
        %14 = sv.reg {name = "Register_inst1"} : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %14, %12 : i1
        }
        sv.initial {
            sv.bpassign %14, %15 : i1
        }
        %13 = sv.read_inout %14 : !hw.inout<i1>
    }
    %11 = hw.constant 0 : i8
    %15 = hw.constant 0 : i1
    hw.output %O_y, %I_x : i1, i8
}
