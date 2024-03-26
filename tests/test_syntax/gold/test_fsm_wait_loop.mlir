module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @Foo(in %n: i8, in %CLK: i1, out O: i16) {
        %1 = hw.struct_create (%0) : !hw.struct<tag: i2>
        %3 = sv.reg name "Register_inst0" : !hw.inout<!hw.struct<tag: i2>>
        sv.alwaysff(posedge %CLK) {
            sv.passign %3, %1 : !hw.struct<tag: i2>
        }
        %5 = hw.constant 0 : i2
        %4 = hw.struct_create (%5) : !hw.struct<tag: i2>
        sv.initial {
            sv.bpassign %3, %4 : !hw.struct<tag: i2>
        }
        %2 = sv.read_inout %3 : !hw.inout<!hw.struct<tag: i2>>
        %6 = hw.struct_extract %2["tag"] : !hw.struct<tag: i2>
        %7 = hw.constant 0 : i2
        %8 = comb.icmp eq %6, %7 : i2
        %9 = hw.constant 65261 : i16
        %10 = hw.constant 2 : i2
        %11 = hw.constant 2 : i2
        %12 = comb.icmp eq %6, %11 : i2
        %13 = hw.constant 57005 : i16
        %16 = sv.reg name "Register_inst1" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %16, %14 : i8
        }
        %17 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %16, %17 : i8
        }
        %15 = sv.read_inout %16 : !hw.inout<i8>
        %20 = sv.reg name "Register_inst2" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %20, %18 : i8
        }
        sv.initial {
            sv.bpassign %20, %17 : i8
        }
        %19 = sv.read_inout %20 : !hw.inout<i8>
        %21 = hw.constant 1 : i8
        %22 = comb.add %19, %21 : i8
        %23 = hw.constant 0 : i8
        %24 = hw.constant 0 : i1
        %25 = hw.constant 1 : i1
        %28 = sv.reg name "Register_inst3" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %28, %26 : i1
        }
        %29 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %28, %29 : i1
        }
        %27 = sv.read_inout %28 : !hw.inout<i1>
        %30 = hw.constant 1 : i8
        %31 = comb.add %19, %30 : i8
        %32 = comb.icmp ult %15, %19 : i8
        %33 = comb.extract %19 from 0 : (i8) -> i1
        %34 = comb.extract %19 from 1 : (i8) -> i1
        %35 = comb.extract %19 from 2 : (i8) -> i1
        %36 = comb.extract %19 from 3 : (i8) -> i1
        %37 = comb.extract %19 from 4 : (i8) -> i1
        %38 = comb.extract %19 from 5 : (i8) -> i1
        %39 = comb.extract %19 from 6 : (i8) -> i1
        %40 = comb.extract %19 from 7 : (i8) -> i1
        %41 = hw.constant 1 : i2
        %42 = hw.constant 1 : i2
        %43 = comb.icmp eq %6, %42 : i2
        %46 = sv.reg name "Register_inst4" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %46, %44 : i1
        }
        sv.initial {
            sv.bpassign %46, %29 : i1
        }
        %45 = sv.read_inout %46 : !hw.inout<i1>
        %47 = hw.constant 3 : i2
        %49 = sv.reg : !hw.inout<i16>
        %48 = sv.read_inout %49 : !hw.inout<i16>
        %50 = sv.reg : !hw.inout<i2>
        %0 = sv.read_inout %50 : !hw.inout<i2>
        %51 = sv.reg : !hw.inout<i8>
        %14 = sv.read_inout %51 : !hw.inout<i8>
        %52 = sv.reg : !hw.inout<i8>
        %18 = sv.read_inout %52 : !hw.inout<i8>
        %53 = sv.reg : !hw.inout<i1>
        %26 = sv.read_inout %53 : !hw.inout<i1>
        %54 = sv.reg : !hw.inout<i1>
        %44 = sv.read_inout %54 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %51, %15 : i8
            sv.bpassign %52, %22 : i8
            sv.bpassign %53, %24 : i1
            sv.bpassign %54, %24 : i1
            sv.bpassign %50, %6 : i2
            sv.if %8 {
                sv.bpassign %50, %10 : i2
                %55 = comb.concat %25, %25, %25, %25, %25, %25, %25, %24, %25, %25, %25, %24, %25, %25, %24, %25 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %49, %55 : i16
            } else {
                sv.if %12 {
                    sv.bpassign %51, %n : i8
                    sv.bpassign %52, %23 : i8
                    sv.bpassign %53, %25 : i1
                    %56 = comb.concat %25, %25, %24, %25, %25, %25, %25, %24, %25, %24, %25, %24, %25, %25, %24, %25 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
                    sv.bpassign %49, %56 : i16
                    sv.if %27 {
                        sv.bpassign %52, %31 : i8
                        sv.if %32 {
                            %57 = comb.concat %24, %24, %24, %24, %24, %24, %24, %24, %40, %39, %38, %37, %36, %35, %34, %33 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
                            sv.bpassign %49, %57 : i16
                        } else {
                            %58 = comb.concat %25, %24, %25, %25, %25, %25, %25, %24, %25, %25, %25, %24, %25, %25, %25, %25 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
                            sv.bpassign %49, %58 : i16
                            sv.bpassign %50, %41 : i2
                        }
                    }
                } else {
                    sv.if %43 {
                        %59 = comb.concat %25, %24, %25, %25, %25, %25, %25, %24, %25, %25, %25, %24, %25, %25, %25, %25 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
                        sv.bpassign %49, %59 : i16
                        sv.bpassign %54, %25 : i1
                        sv.if %45 {
                            %60 = comb.concat %25, %25, %24, %25, %25, %25, %25, %24, %25, %24, %25, %24, %25, %25, %24, %25 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
                            sv.bpassign %49, %60 : i16
                            sv.bpassign %50, %47 : i2
                        }
                    } else {
                        %61 = comb.concat %25, %25, %24, %25, %25, %25, %25, %24, %25, %25, %25, %24, %25, %25, %24, %25 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
                        sv.bpassign %49, %61 : i16
                        sv.bpassign %50, %47 : i2
                    }
                }
            }
        }
        hw.output %48 : i16
    }
}
