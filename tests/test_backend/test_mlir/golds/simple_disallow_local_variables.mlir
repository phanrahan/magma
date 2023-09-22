module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_disallow_local_variables(%x: i2, %s: i1) -> (O: i2) {
        %1 = hw.constant -1 : i1
        %0 = comb.xor %1, %s : i1
        %3 = hw.constant -1 : i2
        %2 = comb.xor %3, %x : i2
        %5 = sv.reg : !hw.inout<i2>
        %4 = sv.read_inout %5 : !hw.inout<i2>
        sv.alwayscomb {
            sv.if %s {
                %8 = comb.concat %7, %6 : i1, i1
                sv.bpassign %5, %8 : i2
            } else {
                %11 = comb.concat %10, %9 : i1, i1
                sv.bpassign %5, %11 : i2
            }
        }
        %6 = comb.extract %2 from 0 : (i2) -> i1
        %7 = comb.extract %2 from 1 : (i2) -> i1
        %9 = comb.extract %x from 0 : (i2) -> i1
        %10 = comb.extract %x from 1 : (i2) -> i1
        %12 = comb.extract %4 from 1 : (i2) -> i1
        %13 = comb.extract %4 from 0 : (i2) -> i1
        %16 = sv.reg : !hw.inout<i1>
        %14 = sv.read_inout %16 : !hw.inout<i1>
        %17 = sv.reg : !hw.inout<i1>
        %15 = sv.read_inout %17 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %0 {
                sv.bpassign %16, %12 : i1
                sv.bpassign %17, %13 : i1
            } else {
                sv.bpassign %16, %13 : i1
                sv.bpassign %17, %12 : i1
            }
        }
        %18 = comb.concat %15, %14 : i1, i1
        hw.output %18 : i2
    }
}
