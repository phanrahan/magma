module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_disallow_local_variables(%x: i2, %s: i1) -> (O: i2) {
        %1 = hw.constant -1 : i1
        %0 = comb.xor %1, %s : i1
        %3 = hw.constant -1 : i2
        %2 = comb.xor %3, %x : i2
        %4 = comb.extract %2 from 0 : (i2) -> i1
        %5 = comb.extract %x from 0 : (i2) -> i1
        %6 = comb.extract %2 from 1 : (i2) -> i1
        %7 = comb.extract %x from 1 : (i2) -> i1
        %11 = sv.reg : !hw.inout<i2>
        %8 = sv.read_inout %11 : !hw.inout<i2>
        %12 = sv.reg : !hw.inout<i1>
        %9 = sv.read_inout %12 : !hw.inout<i1>
        %13 = sv.reg : !hw.inout<i1>
        %10 = sv.read_inout %13 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %s {
                %14 = comb.concat %6, %4 : i1, i1
                sv.bpassign %11, %14 : i2
            } else {
                %15 = comb.concat %7, %5 : i1, i1
                sv.bpassign %11, %15 : i2
            }
        }
        %18 = sv.reg : !hw.inout<i1>
        %16 = sv.read_inout %18 : !hw.inout<i1>
        %19 = sv.reg : !hw.inout<i1>
        %17 = sv.read_inout %19 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %0 {
                sv.bpassign %18, %10 : i1
                sv.bpassign %19, %9 : i1
            } else {
                sv.bpassign %18, %9 : i1
                sv.bpassign %19, %10 : i1
            }
        }
        %20 = comb.concat %17, %16 : i1, i1
        hw.output %20 : i2
    }
}
