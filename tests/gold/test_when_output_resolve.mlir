module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_output_resolve(%I: i8, %x: i1) -> (O0: i8, O1: i2) {
        %1 = sv.wire sym @test_when_output_resolve.x {name="x"} : !hw.inout<i8>
        sv.assign %1, %I : i8
        %0 = sv.read_inout %1 : !hw.inout<i8>
        %3 = hw.constant -1 : i8
        %2 = comb.xor %3, %0 : i8
        %5 = sv.reg : !hw.inout<i8>
        %4 = sv.read_inout %5 : !hw.inout<i8>
        sv.alwayscomb {
            sv.if %x {
                %14 = comb.concat %13, %12, %11, %10, %9, %8, %7, %6 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %5, %14 : i8
            } else {
                %23 = comb.concat %22, %21, %20, %19, %18, %17, %16, %15 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %5, %23 : i8
            }
        }
        %6 = comb.extract %0 from 0 : (i8) -> i1
        %7 = comb.extract %0 from 1 : (i8) -> i1
        %8 = comb.extract %0 from 2 : (i8) -> i1
        %9 = comb.extract %0 from 3 : (i8) -> i1
        %10 = comb.extract %0 from 4 : (i8) -> i1
        %11 = comb.extract %0 from 5 : (i8) -> i1
        %12 = comb.extract %0 from 6 : (i8) -> i1
        %13 = comb.extract %0 from 7 : (i8) -> i1
        %15 = comb.extract %2 from 0 : (i8) -> i1
        %16 = comb.extract %2 from 1 : (i8) -> i1
        %17 = comb.extract %2 from 2 : (i8) -> i1
        %18 = comb.extract %2 from 3 : (i8) -> i1
        %19 = comb.extract %2 from 4 : (i8) -> i1
        %20 = comb.extract %2 from 5 : (i8) -> i1
        %21 = comb.extract %2 from 6 : (i8) -> i1
        %22 = comb.extract %2 from 7 : (i8) -> i1
        %24 = comb.extract %4 from 1 : (i8) -> i1
        %25 = comb.extract %4 from 0 : (i8) -> i1
        %26 = comb.concat %25, %24 : i1, i1
        hw.output %4, %26 : i8, i2
    }
}
