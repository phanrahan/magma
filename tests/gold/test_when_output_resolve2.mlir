module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_output_resolve2(%I: i8, %x: i1) -> (O0: i8, O1: i8) {
        %1 = hw.constant -1 : i8
        %0 = comb.xor %1, %I : i8
        %2 = comb.extract %I from 0 : (i8) -> i1
        %3 = comb.extract %0 from 0 : (i8) -> i1
        %4 = comb.extract %I from 1 : (i8) -> i1
        %5 = comb.extract %0 from 1 : (i8) -> i1
        %6 = comb.extract %I from 2 : (i8) -> i1
        %7 = comb.extract %0 from 2 : (i8) -> i1
        %8 = comb.extract %I from 3 : (i8) -> i1
        %9 = comb.extract %0 from 3 : (i8) -> i1
        %10 = comb.extract %I from 4 : (i8) -> i1
        %11 = comb.extract %0 from 4 : (i8) -> i1
        %12 = comb.extract %I from 5 : (i8) -> i1
        %13 = comb.extract %0 from 5 : (i8) -> i1
        %14 = comb.extract %I from 6 : (i8) -> i1
        %15 = comb.extract %0 from 6 : (i8) -> i1
        %16 = comb.extract %I from 7 : (i8) -> i1
        %17 = comb.extract %0 from 7 : (i8) -> i1
        %27 = sv.reg : !hw.inout<i8>
        %18 = sv.read_inout %27 : !hw.inout<i8>
        %28 = sv.reg : !hw.inout<i1>
        %19 = sv.read_inout %28 : !hw.inout<i1>
        %29 = sv.reg : !hw.inout<i1>
        %20 = sv.read_inout %29 : !hw.inout<i1>
        %30 = sv.reg : !hw.inout<i1>
        %21 = sv.read_inout %30 : !hw.inout<i1>
        %31 = sv.reg : !hw.inout<i1>
        %22 = sv.read_inout %31 : !hw.inout<i1>
        %32 = sv.reg : !hw.inout<i1>
        %23 = sv.read_inout %32 : !hw.inout<i1>
        %33 = sv.reg : !hw.inout<i1>
        %24 = sv.read_inout %33 : !hw.inout<i1>
        %34 = sv.reg : !hw.inout<i1>
        %25 = sv.read_inout %34 : !hw.inout<i1>
        %35 = sv.reg : !hw.inout<i1>
        %26 = sv.read_inout %35 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %x {
                sv.bpassign %28, %2 : i1
                sv.bpassign %29, %4 : i1
                sv.bpassign %30, %6 : i1
                sv.bpassign %31, %8 : i1
                sv.bpassign %32, %10 : i1
                sv.bpassign %33, %12 : i1
                sv.bpassign %34, %14 : i1
                sv.bpassign %35, %16 : i1
            } else {
                sv.bpassign %28, %3 : i1
                sv.bpassign %29, %5 : i1
                sv.bpassign %30, %7 : i1
                sv.bpassign %31, %9 : i1
                sv.bpassign %32, %11 : i1
                sv.bpassign %33, %13 : i1
                sv.bpassign %34, %15 : i1
                sv.bpassign %35, %17 : i1
            }
        }
        %36 = comb.concat %26, %25, %24, %23, %22, %21, %20, %19 : i1, i1, i1, i1, i1, i1, i1, i1
        %37 = comb.concat %26, %25, %24, %23, %22, %21, %20, %19 : i1, i1, i1, i1, i1, i1, i1, i1
        hw.output %36, %37 : i8, i8
    }
}
