module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_tuple_bulk_resolve(%I_x: i8, %I_y_x_x: i8, %I_y_x_y: i8, %I_y_y_x: i8, %I_y_y_y: i8, %S: i2, %CLK: i1) -> (O_x: i8, O_y_x_x: i8, O_y_x_y: i8, O_y_y_x: i8, O_y_y_y: i8) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %11 = sv.reg {name = "y"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %11, %1 : i8
        }
        %12 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %11, %12 : i8
        }
        %6 = sv.read_inout %11 : !hw.inout<i8>
        %13 = sv.reg {name = "y"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %13, %2 : i8
        }
        %14 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %13, %14 : i8
        }
        %7 = sv.read_inout %13 : !hw.inout<i8>
        %15 = sv.reg {name = "y"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %15, %3 : i8
        }
        %16 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %15, %16 : i8
        }
        %8 = sv.read_inout %15 : !hw.inout<i8>
        %17 = sv.reg {name = "y"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %17, %4 : i8
        }
        %18 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %17, %18 : i8
        }
        %9 = sv.read_inout %17 : !hw.inout<i8>
        %19 = sv.reg {name = "y"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %19, %5 : i8
        }
        %20 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %19, %20 : i8
        }
        %10 = sv.read_inout %19 : !hw.inout<i8>
        %21 = comb.extract %S from 1 : (i2) -> i1
        %42 = sv.reg : !hw.inout<i8>
        %27 = sv.read_inout %42 : !hw.inout<i8>
        %43 = sv.reg : !hw.inout<i8>
        %28 = sv.read_inout %43 : !hw.inout<i8>
        %44 = sv.reg : !hw.inout<i8>
        %29 = sv.read_inout %44 : !hw.inout<i8>
        %45 = sv.reg : !hw.inout<i8>
        %30 = sv.read_inout %45 : !hw.inout<i8>
        %46 = sv.reg : !hw.inout<i8>
        %31 = sv.read_inout %46 : !hw.inout<i8>
        %47 = sv.reg : !hw.inout<i8>
        %32 = sv.read_inout %47 : !hw.inout<i8>
        %48 = sv.reg : !hw.inout<i8>
        %33 = sv.read_inout %48 : !hw.inout<i8>
        %49 = sv.reg : !hw.inout<i8>
        %34 = sv.read_inout %49 : !hw.inout<i8>
        %50 = sv.reg : !hw.inout<i8>
        %35 = sv.read_inout %50 : !hw.inout<i8>
        %51 = sv.reg : !hw.inout<i8>
        %36 = sv.read_inout %51 : !hw.inout<i8>
        %52 = sv.reg : !hw.inout<i8>
        %37 = sv.read_inout %52 : !hw.inout<i8>
        %53 = sv.reg : !hw.inout<i8>
        %38 = sv.read_inout %53 : !hw.inout<i8>
        %54 = sv.reg : !hw.inout<i8>
        %39 = sv.read_inout %54 : !hw.inout<i8>
        %55 = sv.reg : !hw.inout<i8>
        %40 = sv.read_inout %55 : !hw.inout<i8>
        %56 = sv.reg : !hw.inout<i8>
        %41 = sv.read_inout %56 : !hw.inout<i8>
        %57 = sv.reg : !hw.inout<i8>
        %1 = sv.read_inout %57 : !hw.inout<i8>
        %58 = sv.reg : !hw.inout<i8>
        %2 = sv.read_inout %58 : !hw.inout<i8>
        %59 = sv.reg : !hw.inout<i8>
        %3 = sv.read_inout %59 : !hw.inout<i8>
        %60 = sv.reg : !hw.inout<i8>
        %4 = sv.read_inout %60 : !hw.inout<i8>
        %61 = sv.reg : !hw.inout<i8>
        %5 = sv.read_inout %61 : !hw.inout<i8>
        sv.alwayscomb {
            sv.if %0 {
                sv.bpassign %52, %22 : i8
                sv.bpassign %53, %23 : i8
                sv.bpassign %54, %24 : i8
                sv.bpassign %55, %25 : i8
                sv.bpassign %56, %26 : i8
                sv.bpassign %57, %6 : i8
                sv.bpassign %58, %7 : i8
                sv.bpassign %59, %8 : i8
                sv.bpassign %60, %9 : i8
                sv.bpassign %61, %10 : i8
            } else {
                sv.bpassign %57, %22 : i8
                sv.bpassign %58, %23 : i8
                sv.bpassign %59, %24 : i8
                sv.bpassign %60, %25 : i8
                sv.bpassign %61, %26 : i8
                sv.if %21 {
                    sv.bpassign %52, %I_x : i8
                    sv.bpassign %53, %I_y_x_x : i8
                    sv.bpassign %54, %I_y_x_y : i8
                    sv.bpassign %55, %I_y_y_x : i8
                    sv.bpassign %56, %I_y_y_y : i8
                } else {
                    sv.bpassign %52, %22 : i8
                    sv.bpassign %53, %23 : i8
                    sv.bpassign %54, %24 : i8
                    sv.bpassign %55, %25 : i8
                    sv.bpassign %56, %26 : i8
                }
            }
        }
        %62 = sv.reg {name = "x"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %62, %37 : i8
        }
        sv.initial {
            sv.bpassign %62, %12 : i8
        }
        %22 = sv.read_inout %62 : !hw.inout<i8>
        %63 = sv.reg {name = "x"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %63, %38 : i8
        }
        sv.initial {
            sv.bpassign %63, %14 : i8
        }
        %23 = sv.read_inout %63 : !hw.inout<i8>
        %64 = sv.reg {name = "x"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %64, %39 : i8
        }
        sv.initial {
            sv.bpassign %64, %16 : i8
        }
        %24 = sv.read_inout %64 : !hw.inout<i8>
        %65 = sv.reg {name = "x"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %65, %40 : i8
        }
        sv.initial {
            sv.bpassign %65, %18 : i8
        }
        %25 = sv.read_inout %65 : !hw.inout<i8>
        %66 = sv.reg {name = "x"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %66, %41 : i8
        }
        sv.initial {
            sv.bpassign %66, %20 : i8
        }
        %26 = sv.read_inout %66 : !hw.inout<i8>
        hw.output %22, %23, %24, %25, %26 : i8, i8, i8, i8, i8
    }
}
