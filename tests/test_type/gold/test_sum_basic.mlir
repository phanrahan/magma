hw.module @Foo(%I_tag: i1, %I_data: i2) -> (O_tag: i1, O_data: i2) {
    %0 = hw.constant 0 : i1
    %1 = comb.icmp eq %I_tag, %0 : i1
    %2 = hw.constant 0 : i1
    %3 = comb.extract %I_data from 0 : (i2) -> i1
    %5 = hw.constant -1 : i1
    %4 = comb.xor %5, %3 : i1
    %6 = hw.constant 0 : i1
    %7 = hw.constant 1 : i1
    %9 = hw.constant -1 : i2
    %8 = comb.xor %9, %I_data : i2
    %10 = hw.constant 3 : i2
    %11 = comb.xor %8, %10 : i2
    %12 = comb.extract %11 from 0 : (i2) -> i1
    %13 = comb.extract %11 from 1 : (i2) -> i1
    %17 = sv.reg {name = "Foo.O.tag_reg"} : !hw.inout<i1>
    %18 = sv.reg {name = "Foo.O.data[0]_reg"} : !hw.inout<i1>
    %19 = sv.reg {name = "Foo.O.data[1]_reg"} : !hw.inout<i1>
    sv.alwayscomb {
        sv.if %1 {
            sv.bpassign %17, %2 : i1
            sv.bpassign %18, %4 : i1
            sv.bpassign %19, %6 : i1
        } else {
            sv.bpassign %17, %7 : i1
            sv.bpassign %18, %12 : i1
            sv.bpassign %19, %13 : i1
        }
    }
    %14 = sv.read_inout %17 : !hw.inout<i1>
    %15 = sv.read_inout %18 : !hw.inout<i1>
    %16 = sv.read_inout %19 : !hw.inout<i1>
    %20 = comb.concat %16, %15 : i1, i1
    hw.output %14, %20 : i1, i2
}
