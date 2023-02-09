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
        %10 = comb.extract %8 from 0 : (i8) -> i1
        %11 = comb.extract %I from 0 : (i8) -> i1
        %12 = comb.extract %8 from 1 : (i8) -> i1
        %13 = comb.extract %I from 1 : (i8) -> i1
        %14 = comb.extract %8 from 2 : (i8) -> i1
        %15 = comb.extract %I from 2 : (i8) -> i1
        %16 = comb.extract %8 from 3 : (i8) -> i1
        %17 = comb.extract %I from 3 : (i8) -> i1
        %18 = comb.extract %8 from 4 : (i8) -> i1
        %19 = comb.extract %I from 4 : (i8) -> i1
        %20 = comb.extract %8 from 5 : (i8) -> i1
        %21 = comb.extract %I from 5 : (i8) -> i1
        %22 = comb.extract %8 from 6 : (i8) -> i1
        %23 = comb.extract %I from 6 : (i8) -> i1
        %24 = comb.extract %8 from 7 : (i8) -> i1
        %25 = comb.extract %I from 7 : (i8) -> i1
        %35 = sv.reg : !hw.inout<i8>
        %26 = sv.read_inout %35 : !hw.inout<i8>
        %36 = sv.reg : !hw.inout<i1>
        %27 = sv.read_inout %36 : !hw.inout<i1>
        %37 = sv.reg : !hw.inout<i1>
        %28 = sv.read_inout %37 : !hw.inout<i1>
        %38 = sv.reg : !hw.inout<i1>
        %29 = sv.read_inout %38 : !hw.inout<i1>
        %39 = sv.reg : !hw.inout<i1>
        %30 = sv.read_inout %39 : !hw.inout<i1>
        %40 = sv.reg : !hw.inout<i1>
        %31 = sv.read_inout %40 : !hw.inout<i1>
        %41 = sv.reg : !hw.inout<i1>
        %32 = sv.read_inout %41 : !hw.inout<i1>
        %42 = sv.reg : !hw.inout<i1>
        %33 = sv.read_inout %42 : !hw.inout<i1>
        %43 = sv.reg : !hw.inout<i1>
        %34 = sv.read_inout %43 : !hw.inout<i1>
        sv.alwayscomb {
            %44 = comb.concat %24, %22, %20, %18, %16, %14, %12, %10 : i1, i1, i1, i1, i1, i1, i1, i1
            sv.bpassign %35, %44 : i8
            sv.if %S {
                %45 = comb.concat %25, %23, %21, %19, %17, %15, %13, %11 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %35, %45 : i8
            }
        }
        %46 = comb.concat %34, %33, %32, %31, %30, %29, %28, %27, %7, %6, %5, %4, %3, %2, %1, %0 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        hw.output %46 : i16
    }
}
