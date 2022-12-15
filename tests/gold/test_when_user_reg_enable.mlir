module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module.extern @Register(%I: i8, %CE: i1, %CLK: i1) -> (O: i8)
    hw.module @test_when_user_reg_enable(%I: i8, %x: i2, %CLK: i1) -> (O: i8) {
        %0 = comb.extract %x from 0 : (i2) -> i1
        %1 = comb.extract %I from 0 : (i8) -> i1
        %2 = comb.extract %I from 1 : (i8) -> i1
        %3 = comb.extract %I from 2 : (i8) -> i1
        %4 = comb.extract %I from 3 : (i8) -> i1
        %5 = comb.extract %I from 4 : (i8) -> i1
        %6 = comb.extract %I from 5 : (i8) -> i1
        %7 = comb.extract %I from 6 : (i8) -> i1
        %8 = comb.extract %I from 7 : (i8) -> i1
        %9 = hw.constant 1 : i1
        %10 = comb.extract %x from 1 : (i2) -> i1
        %12 = hw.constant -1 : i8
        %11 = comb.xor %12, %I : i8
        %13 = comb.extract %11 from 0 : (i8) -> i1
        %14 = comb.extract %11 from 1 : (i8) -> i1
        %15 = comb.extract %11 from 2 : (i8) -> i1
        %16 = comb.extract %11 from 3 : (i8) -> i1
        %17 = comb.extract %11 from 4 : (i8) -> i1
        %18 = comb.extract %11 from 5 : (i8) -> i1
        %19 = comb.extract %11 from 6 : (i8) -> i1
        %20 = comb.extract %11 from 7 : (i8) -> i1
        %22 = comb.extract %21 from 0 : (i8) -> i1
        %23 = comb.extract %21 from 1 : (i8) -> i1
        %24 = comb.extract %21 from 2 : (i8) -> i1
        %25 = comb.extract %21 from 3 : (i8) -> i1
        %26 = comb.extract %21 from 4 : (i8) -> i1
        %27 = comb.extract %21 from 5 : (i8) -> i1
        %28 = comb.extract %21 from 6 : (i8) -> i1
        %29 = comb.extract %21 from 7 : (i8) -> i1
        %30 = hw.constant 0 : i1
        %40 = sv.reg : !hw.inout<i1>
        %31 = sv.read_inout %40 : !hw.inout<i1>
        %41 = sv.reg : !hw.inout<i1>
        %32 = sv.read_inout %41 : !hw.inout<i1>
        %42 = sv.reg : !hw.inout<i1>
        %33 = sv.read_inout %42 : !hw.inout<i1>
        %43 = sv.reg : !hw.inout<i1>
        %34 = sv.read_inout %43 : !hw.inout<i1>
        %44 = sv.reg : !hw.inout<i1>
        %35 = sv.read_inout %44 : !hw.inout<i1>
        %45 = sv.reg : !hw.inout<i1>
        %36 = sv.read_inout %45 : !hw.inout<i1>
        %46 = sv.reg : !hw.inout<i1>
        %37 = sv.read_inout %46 : !hw.inout<i1>
        %47 = sv.reg : !hw.inout<i1>
        %38 = sv.read_inout %47 : !hw.inout<i1>
        %48 = sv.reg : !hw.inout<i1>
        %39 = sv.read_inout %48 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %40, %22 : i1
            sv.bpassign %41, %23 : i1
            sv.bpassign %42, %24 : i1
            sv.bpassign %43, %25 : i1
            sv.bpassign %44, %26 : i1
            sv.bpassign %45, %27 : i1
            sv.bpassign %46, %28 : i1
            sv.bpassign %47, %29 : i1
            sv.bpassign %48, %30 : i1
            sv.if %0 {
                sv.bpassign %40, %1 : i1
                sv.bpassign %41, %2 : i1
                sv.bpassign %42, %3 : i1
                sv.bpassign %43, %4 : i1
                sv.bpassign %44, %5 : i1
                sv.bpassign %45, %6 : i1
                sv.bpassign %46, %7 : i1
                sv.bpassign %47, %8 : i1
                sv.bpassign %48, %9 : i1
            } else {
                sv.if %10 {
                    sv.bpassign %40, %13 : i1
                    sv.bpassign %41, %14 : i1
                    sv.bpassign %42, %15 : i1
                    sv.bpassign %43, %16 : i1
                    sv.bpassign %44, %17 : i1
                    sv.bpassign %45, %18 : i1
                    sv.bpassign %46, %19 : i1
                    sv.bpassign %47, %20 : i1
                    sv.bpassign %48, %9 : i1
                }
            }
        }
        %49 = comb.concat %38, %37, %36, %35, %34, %33, %32, %31 : i1, i1, i1, i1, i1, i1, i1, i1
        %21 = hw.instance "Register_inst0" @Register(I: %49: i8, CE: %39: i1, CLK: %CLK: i1) -> (O: i8)
        hw.output %21 : i8
    }
}
