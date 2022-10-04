hw.module @Foo(%I0_tag: i1, %I0_data: i2, %I1: i2) -> (O0_tag: i1, O0_data: i2, O1: i2, O2_tag: i1, O2_data: i2) {
    %0 = hw.constant 0 : i1
    %1 = comb.icmp eq %I0_tag, %0 : i1
    %2 = hw.constant 0 : i1
    %3 = comb.extract %I0_data from 0 : (i2) -> i1
    %5 = hw.constant -1 : i1
    %4 = comb.xor %5, %3 : i1
    %6 = hw.constant 0 : i1
    %7 = hw.constant 0 : i1
    %8 = comb.extract %I1 from 1 : (i2) -> i1
    %9 = comb.extract %I1 from 0 : (i2) -> i1
    %10 = comb.xor %8, %9 : i1
    %11 = hw.constant 1 : i1
    %12 = hw.constant 3 : i2
    %13 = comb.xor %I0_data, %12 : i2
    %14 = comb.extract %13 from 0 : (i2) -> i1
    %15 = comb.extract %13 from 1 : (i2) -> i1
    %16 = hw.constant 1 : i2
    %17 = comb.and %I0_data, %16 : i2
    %18 = comb.extract %17 from 0 : (i2) -> i1
    %19 = comb.extract %17 from 1 : (i2) -> i1
    %20 = hw.constant 1 : i1
    %21 = hw.constant 2 : i2
    %22 = comb.or %I1, %21 : i2
    %23 = comb.extract %22 from 0 : (i2) -> i1
    %24 = comb.extract %22 from 1 : (i2) -> i1
    %33 = sv.reg : !hw.inout<i1>
    %25 = sv.read_inout %33 : !hw.inout<i1>
    %34 = sv.reg : !hw.inout<i1>
    %26 = sv.read_inout %34 : !hw.inout<i1>
    %35 = sv.reg : !hw.inout<i1>
    %27 = sv.read_inout %35 : !hw.inout<i1>
    %36 = sv.reg : !hw.inout<i1>
    %28 = sv.read_inout %36 : !hw.inout<i1>
    %37 = sv.reg : !hw.inout<i1>
    %29 = sv.read_inout %37 : !hw.inout<i1>
    %38 = sv.reg : !hw.inout<i1>
    %30 = sv.read_inout %38 : !hw.inout<i1>
    %39 = sv.reg : !hw.inout<i1>
    %31 = sv.read_inout %39 : !hw.inout<i1>
    %40 = sv.reg : !hw.inout<i1>
    %32 = sv.read_inout %40 : !hw.inout<i1>
    sv.alwayscomb {
        sv.if %1 {
            sv.bpassign %33, %2 : i1
            sv.bpassign %34, %4 : i1
            sv.bpassign %35, %6 : i1
            sv.bpassign %36, %3 : i1
            sv.bpassign %37, %6 : i1
            sv.bpassign %38, %7 : i1
            sv.bpassign %39, %10 : i1
            sv.bpassign %40, %6 : i1
        } else {
            sv.bpassign %33, %11 : i1
            sv.bpassign %34, %14 : i1
            sv.bpassign %35, %15 : i1
            sv.bpassign %36, %18 : i1
            sv.bpassign %37, %19 : i1
            sv.bpassign %38, %20 : i1
            sv.bpassign %39, %23 : i1
            sv.bpassign %40, %24 : i1
        }
    }
    %41 = comb.concat %27, %26 : i1, i1
    %42 = comb.concat %29, %28 : i1, i1
    %43 = comb.concat %32, %31 : i1, i1
    hw.output %25, %41, %42, %30, %43 : i1, i2, i2, i1, i2
}
