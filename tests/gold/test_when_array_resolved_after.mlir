module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_array_resolved_after(%I: i8, %S: i1) -> (O: i16) {
        %0 = hw.constant 0 : i1
        %1 = hw.constant 0 : i1
        %2 = hw.constant 0 : i1
        %3 = hw.constant 0 : i1
        %4 = hw.constant 0 : i1
        %5 = hw.constant 0 : i1
        %6 = hw.constant 0 : i1
        %7 = hw.constant 0 : i1
        %9 = hw.constant -1 : i8
        %8 = comb.xor %9, %I : i8
        %11 = sv.reg : !hw.inout<i8>
        %10 = sv.read_inout %11 : !hw.inout<i8>
        sv.alwayscomb {
            %12 = comb.extract %8 from 0 : (i8) -> i1
            %13 = comb.extract %8 from 1 : (i8) -> i1
            %14 = comb.extract %8 from 2 : (i8) -> i1
            %15 = comb.extract %8 from 3 : (i8) -> i1
            %16 = comb.extract %8 from 4 : (i8) -> i1
            %17 = comb.extract %8 from 5 : (i8) -> i1
            %18 = comb.extract %8 from 6 : (i8) -> i1
            %19 = comb.extract %8 from 7 : (i8) -> i1
            %20 = comb.concat %19, %18, %17, %16, %15, %14, %13, %12 : i1, i1, i1, i1, i1, i1, i1, i1
            sv.bpassign %11, %20 : i8
            sv.if %S {
                %21 = comb.extract %I from 0 : (i8) -> i1
                %22 = comb.extract %I from 1 : (i8) -> i1
                %23 = comb.extract %I from 2 : (i8) -> i1
                %24 = comb.extract %I from 3 : (i8) -> i1
                %25 = comb.extract %I from 4 : (i8) -> i1
                %26 = comb.extract %I from 5 : (i8) -> i1
                %27 = comb.extract %I from 6 : (i8) -> i1
                %28 = comb.extract %I from 7 : (i8) -> i1
                %29 = comb.concat %28, %27, %26, %25, %24, %23, %22, %21 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %11, %29 : i8
            }
        }
        %30 = comb.extract %10 from 0 : (i8) -> i1
        %31 = comb.extract %10 from 1 : (i8) -> i1
        %32 = comb.extract %10 from 2 : (i8) -> i1
        %33 = comb.extract %10 from 3 : (i8) -> i1
        %34 = comb.extract %10 from 4 : (i8) -> i1
        %35 = comb.extract %10 from 5 : (i8) -> i1
        %36 = comb.extract %10 from 6 : (i8) -> i1
        %37 = comb.extract %10 from 7 : (i8) -> i1
        %38 = comb.concat %37, %36, %35, %34, %33, %32, %31, %30, %7, %6, %5, %4, %3, %2, %1, %0 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        hw.output %38 : i16
    }
}
