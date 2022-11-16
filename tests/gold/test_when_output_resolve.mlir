module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_output_resolve(%I: i8, %x: i1) -> (O0: i8, O1: i2) {
        %1 = sv.wire sym @test_when_output_resolve.x {name="x"} : !hw.inout<i8>
        sv.assign %1, %I : i8
        %0 = sv.read_inout %1 : !hw.inout<i8>
        %3 = hw.constant -1 : i8
        %2 = comb.xor %3, %0 : i8
        %4 = comb.extract %0 from 0 : (i8) -> i1
        %5 = comb.extract %2 from 0 : (i8) -> i1
        %6 = comb.extract %0 from 1 : (i8) -> i1
        %7 = comb.extract %2 from 1 : (i8) -> i1
        %8 = comb.extract %0 from 2 : (i8) -> i1
        %9 = comb.extract %2 from 2 : (i8) -> i1
        %10 = comb.extract %0 from 3 : (i8) -> i1
        %11 = comb.extract %2 from 3 : (i8) -> i1
        %12 = comb.extract %0 from 4 : (i8) -> i1
        %13 = comb.extract %2 from 4 : (i8) -> i1
        %14 = comb.extract %0 from 5 : (i8) -> i1
        %15 = comb.extract %2 from 5 : (i8) -> i1
        %16 = comb.extract %0 from 6 : (i8) -> i1
        %17 = comb.extract %2 from 6 : (i8) -> i1
        %18 = comb.extract %0 from 7 : (i8) -> i1
        %19 = comb.extract %2 from 7 : (i8) -> i1
        %29 = sv.reg : !hw.inout<i8>
        %20 = sv.read_inout %29 : !hw.inout<i8>
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
        %36 = sv.reg : !hw.inout<i1>
        %27 = sv.read_inout %36 : !hw.inout<i1>
        %37 = sv.reg : !hw.inout<i1>
        %28 = sv.read_inout %37 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %x {
                sv.bpassign %30, %4 : i1
                sv.bpassign %31, %6 : i1
                sv.bpassign %32, %8 : i1
                sv.bpassign %33, %10 : i1
                sv.bpassign %34, %12 : i1
                sv.bpassign %35, %14 : i1
                sv.bpassign %36, %16 : i1
                sv.bpassign %37, %18 : i1
            } else {
                sv.bpassign %30, %5 : i1
                sv.bpassign %31, %7 : i1
                sv.bpassign %32, %9 : i1
                sv.bpassign %33, %11 : i1
                sv.bpassign %34, %13 : i1
                sv.bpassign %35, %15 : i1
                sv.bpassign %36, %17 : i1
                sv.bpassign %37, %19 : i1
            }
        }
        %38 = comb.concat %28, %27, %26, %25, %24, %23, %22, %21 : i1, i1, i1, i1, i1, i1, i1, i1
        %39 = comb.concat %21, %22 : i1, i1
        hw.output %38, %39 : i8, i2
    }
}
