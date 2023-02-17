module attributes {circt.loweringOptions = "locationInfoStyle=none,disallowLocalVariables"} {
    hw.module @test_when_temporary_resolved(%I: i8, %S: i2, %CLK: i1) -> (O: i8) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %3 = sv.reg {name = "Register_inst0"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %3, %1 : i8
        }
        %4 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %3, %4 : i8
        }
        %2 = sv.read_inout %3 : !hw.inout<i8>
        %5 = hw.constant 4 : i8
        %6 = comb.sub %2, %5 : i8
        %7 = comb.extract %S from 1 : (i2) -> i1
        %8 = comb.extract %2 from 0 : (i8) -> i1
        %9 = comb.extract %2 from 1 : (i8) -> i1
        %10 = comb.extract %2 from 2 : (i8) -> i1
        %11 = comb.extract %2 from 3 : (i8) -> i1
        %12 = comb.extract %2 from 4 : (i8) -> i1
        %13 = comb.extract %2 from 5 : (i8) -> i1
        %14 = comb.extract %2 from 6 : (i8) -> i1
        %15 = comb.extract %2 from 7 : (i8) -> i1
        %16 = hw.constant 0 : i1
        %17 = comb.concat %16, %15, %14, %13, %12, %11, %10, %9, %8 : i1, i1, i1, i1, i1, i1, i1, i1, i1
        %18 = comb.extract %I from 0 : (i8) -> i1
        %19 = comb.extract %I from 1 : (i8) -> i1
        %20 = comb.extract %I from 2 : (i8) -> i1
        %21 = comb.extract %I from 3 : (i8) -> i1
        %22 = comb.extract %I from 4 : (i8) -> i1
        %23 = comb.extract %I from 5 : (i8) -> i1
        %24 = comb.extract %I from 6 : (i8) -> i1
        %25 = comb.extract %I from 7 : (i8) -> i1
        %26 = hw.constant 0 : i1
        %27 = comb.concat %26, %25, %24, %23, %22, %21, %20, %19, %18 : i1, i1, i1, i1, i1, i1, i1, i1, i1
        %28 = comb.add %17, %27 : i9
        %29 = comb.extract %28 from 0 : (i9) -> i1
        %30 = comb.extract %28 from 1 : (i9) -> i1
        %31 = comb.extract %28 from 2 : (i9) -> i1
        %32 = comb.extract %28 from 3 : (i9) -> i1
        %33 = comb.extract %28 from 4 : (i9) -> i1
        %34 = comb.extract %28 from 5 : (i9) -> i1
        %35 = comb.extract %28 from 6 : (i9) -> i1
        %36 = comb.extract %28 from 7 : (i9) -> i1
        %37 = comb.concat %36, %35, %34, %33, %32, %31, %30, %29 : i1, i1, i1, i1, i1, i1, i1, i1
        %38 = comb.concat %36, %35, %34, %33, %32, %31, %30, %29 : i1, i1, i1, i1, i1, i1, i1, i1
        %39 = hw.constant 4 : i8
        %40 = comb.sub %38, %39 : i8
        %41 = sv.reg : !hw.inout<i8>
        %1 = sv.read_inout %41 : !hw.inout<i8>
        sv.alwayscomb {
            sv.if %0 {
                %50 = comb.concat %49, %48, %47, %46, %45, %44, %43, %42 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %41, %50 : i8
            } else {
                sv.if %7 {
                    %51 = comb.concat %36, %35, %34, %33, %32, %31, %30, %29 : i1, i1, i1, i1, i1, i1, i1, i1
                    sv.bpassign %41, %51 : i8
                } else {
                    %60 = comb.concat %59, %58, %57, %56, %55, %54, %53, %52 : i1, i1, i1, i1, i1, i1, i1, i1
                    sv.bpassign %41, %60 : i8
                }
            }
        }
        %42 = comb.extract %6 from 0 : (i8) -> i1
        %43 = comb.extract %6 from 1 : (i8) -> i1
        %44 = comb.extract %6 from 2 : (i8) -> i1
        %45 = comb.extract %6 from 3 : (i8) -> i1
        %46 = comb.extract %6 from 4 : (i8) -> i1
        %47 = comb.extract %6 from 5 : (i8) -> i1
        %48 = comb.extract %6 from 6 : (i8) -> i1
        %49 = comb.extract %6 from 7 : (i8) -> i1
        %52 = comb.extract %40 from 0 : (i8) -> i1
        %53 = comb.extract %40 from 1 : (i8) -> i1
        %54 = comb.extract %40 from 2 : (i8) -> i1
        %55 = comb.extract %40 from 3 : (i8) -> i1
        %56 = comb.extract %40 from 4 : (i8) -> i1
        %57 = comb.extract %40 from 5 : (i8) -> i1
        %58 = comb.extract %40 from 6 : (i8) -> i1
        %59 = comb.extract %40 from 7 : (i8) -> i1
        hw.output %1 : i8
    }
}
