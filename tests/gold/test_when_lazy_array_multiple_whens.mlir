hw.module @test_when_lazy_array_multiple_whens(%I: i4, %S: i1) -> (O: i4) {
    %1 = hw.constant -1 : i1
    %0 = comb.xor %1, %S : i1
    %2 = comb.extract %I from 0 : (i4) -> i1
    %3 = comb.extract %I from 1 : (i4) -> i1
    %4 = comb.extract %I from 2 : (i4) -> i1
    %5 = comb.extract %I from 3 : (i4) -> i1
    %10 = sv.reg : !hw.inout<i1>
    %6 = sv.read_inout %10 : !hw.inout<i1>
    %11 = sv.reg : !hw.inout<i1>
    %7 = sv.read_inout %11 : !hw.inout<i1>
    %12 = sv.reg : !hw.inout<i1>
    %8 = sv.read_inout %12 : !hw.inout<i1>
    %13 = sv.reg : !hw.inout<i1>
    %9 = sv.read_inout %13 : !hw.inout<i1>
    sv.alwayscomb {
        sv.if %S {
            sv.bpassign %10, %2 : i1
            sv.bpassign %11, %3 : i1
            sv.bpassign %12, %4 : i1
            sv.bpassign %13, %5 : i1
        } else {
            sv.bpassign %10, %4 : i1
            sv.bpassign %11, %5 : i1
            sv.bpassign %12, %2 : i1
            sv.bpassign %13, %3 : i1
        }
    }
    %18 = sv.reg : !hw.inout<i1>
    %14 = sv.read_inout %18 : !hw.inout<i1>
    %19 = sv.reg : !hw.inout<i1>
    %15 = sv.read_inout %19 : !hw.inout<i1>
    %20 = sv.reg : !hw.inout<i1>
    %16 = sv.read_inout %20 : !hw.inout<i1>
    %21 = sv.reg : !hw.inout<i1>
    %17 = sv.read_inout %21 : !hw.inout<i1>
    sv.alwayscomb {
        sv.bpassign %18, %6 : i1
        sv.bpassign %19, %7 : i1
        sv.bpassign %20, %8 : i1
        sv.bpassign %21, %9 : i1
        sv.if %0 {
            sv.bpassign %18, %2 : i1
            sv.bpassign %19, %3 : i1
            sv.bpassign %20, %4 : i1
            sv.bpassign %21, %5 : i1
        }
    }
    %22 = comb.concat %17, %16, %15, %14 : i1, i1, i1, i1
    hw.output %22 : i4
}
