module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @Gen(%a: i8) -> (y: i8) {
        %0 = comb.extract %a from 0 : (i8) -> i1
        %1 = comb.extract %a from 1 : (i8) -> i1
        %2 = hw.constant 0 : i1
        %3 = comb.extract %a from 2 : (i8) -> i1
        %4 = comb.extract %a from 3 : (i8) -> i1
        %5 = comb.extract %a from 4 : (i8) -> i1
        %6 = comb.extract %a from 5 : (i8) -> i1
        %7 = comb.extract %a from 6 : (i8) -> i1
        %8 = comb.extract %a from 7 : (i8) -> i1
        %17 = sv.reg : !hw.inout<i1>
        %9 = sv.read_inout %17 : !hw.inout<i1>
        %18 = sv.reg : !hw.inout<i1>
        %10 = sv.read_inout %18 : !hw.inout<i1>
        %19 = sv.reg : !hw.inout<i1>
        %11 = sv.read_inout %19 : !hw.inout<i1>
        %20 = sv.reg : !hw.inout<i1>
        %12 = sv.read_inout %20 : !hw.inout<i1>
        %21 = sv.reg : !hw.inout<i1>
        %13 = sv.read_inout %21 : !hw.inout<i1>
        %22 = sv.reg : !hw.inout<i1>
        %14 = sv.read_inout %22 : !hw.inout<i1>
        %23 = sv.reg : !hw.inout<i1>
        %15 = sv.read_inout %23 : !hw.inout<i1>
        %24 = sv.reg : !hw.inout<i1>
        %16 = sv.read_inout %24 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %0 {
                sv.bpassign %17, %0 : i1
                sv.bpassign %18, %1 : i1
                sv.bpassign %19, %2 : i1
                sv.bpassign %20, %2 : i1
                sv.bpassign %21, %2 : i1
                sv.bpassign %22, %2 : i1
                sv.bpassign %23, %2 : i1
                sv.bpassign %24, %2 : i1
            } else {
                sv.bpassign %17, %0 : i1
                sv.bpassign %18, %1 : i1
                sv.bpassign %19, %3 : i1
                sv.bpassign %20, %4 : i1
                sv.bpassign %21, %5 : i1
                sv.bpassign %22, %6 : i1
                sv.bpassign %23, %7 : i1
                sv.bpassign %24, %8 : i1
            }
        }
        %25 = comb.concat %16, %15, %14, %13, %12, %11, %10, %9 : i1, i1, i1, i1, i1, i1, i1, i1
        hw.output %25 : i8
    }
    hw.module @Gen_unq1(%a: i8) -> (y: i8) {
        %0 = comb.extract %a from 0 : (i8) -> i1
        %1 = comb.extract %a from 1 : (i8) -> i1
        %2 = comb.extract %a from 2 : (i8) -> i1
        %3 = comb.extract %a from 3 : (i8) -> i1
        %4 = hw.constant 0 : i1
        %5 = comb.extract %a from 4 : (i8) -> i1
        %6 = comb.extract %a from 5 : (i8) -> i1
        %7 = comb.extract %a from 6 : (i8) -> i1
        %8 = comb.extract %a from 7 : (i8) -> i1
        %17 = sv.reg : !hw.inout<i1>
        %9 = sv.read_inout %17 : !hw.inout<i1>
        %18 = sv.reg : !hw.inout<i1>
        %10 = sv.read_inout %18 : !hw.inout<i1>
        %19 = sv.reg : !hw.inout<i1>
        %11 = sv.read_inout %19 : !hw.inout<i1>
        %20 = sv.reg : !hw.inout<i1>
        %12 = sv.read_inout %20 : !hw.inout<i1>
        %21 = sv.reg : !hw.inout<i1>
        %13 = sv.read_inout %21 : !hw.inout<i1>
        %22 = sv.reg : !hw.inout<i1>
        %14 = sv.read_inout %22 : !hw.inout<i1>
        %23 = sv.reg : !hw.inout<i1>
        %15 = sv.read_inout %23 : !hw.inout<i1>
        %24 = sv.reg : !hw.inout<i1>
        %16 = sv.read_inout %24 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %0 {
                sv.bpassign %17, %0 : i1
                sv.bpassign %18, %1 : i1
                sv.bpassign %19, %2 : i1
                sv.bpassign %20, %3 : i1
                sv.bpassign %21, %4 : i1
                sv.bpassign %22, %4 : i1
                sv.bpassign %23, %4 : i1
                sv.bpassign %24, %4 : i1
            } else {
                sv.bpassign %17, %0 : i1
                sv.bpassign %18, %1 : i1
                sv.bpassign %19, %2 : i1
                sv.bpassign %20, %3 : i1
                sv.bpassign %21, %5 : i1
                sv.bpassign %22, %6 : i1
                sv.bpassign %23, %7 : i1
                sv.bpassign %24, %8 : i1
            }
        }
        %25 = comb.concat %16, %15, %14, %13, %12, %11, %10, %9 : i1, i1, i1, i1, i1, i1, i1, i1
        hw.output %25 : i8
    }
    hw.module @test_when_unique(%a: i8) -> (y: i8) {
        %0 = hw.instance "Gen_inst0" @Gen(a: %a: i8) -> (y: i8)
        %1 = hw.instance "Gen_inst1" @Gen_unq1(a: %a: i8) -> (y: i8)
        %2 = comb.or %0, %1 : i8
        hw.output %2 : i8
    }
}
