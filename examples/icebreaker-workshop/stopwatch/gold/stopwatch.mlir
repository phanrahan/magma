module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @Counter(in %CLK: i1, out O: i21, out COUT: i1) {
        %0 = hw.constant 1 : i21
        %2 = comb.add %1, %0 : i21
        %3 = hw.constant 0 : i21
        %4 = hw.constant 1199999 : i21
        %5 = comb.icmp eq %1, %4 : i21
        %7 = hw.array_create %3, %2 : i21
        %6 = hw.array_get %7[%5] : !hw.array<2xi21>, i1
        %8 = sv.reg name "Register_inst0" : !hw.inout<i21>
        sv.alwaysff(posedge %CLK) {
            sv.passign %8, %6 : i21
        }
        %9 = hw.constant 0 : i21
        sv.initial {
            sv.bpassign %8, %9 : i21
        }
        %1 = sv.read_inout %8 : !hw.inout<i21>
        %10 = hw.constant 1199999 : i21
        %11 = comb.icmp eq %1, %10 : i21
        hw.output %1, %11 : i21, i1
    }
    hw.module @bcd8_increment(in %din: i8, out dout: i8) {
        %0 = hw.constant 153 : i8
        %1 = comb.icmp eq %din, %0 : i8
        %2 = hw.constant 0 : i8
        %3 = comb.extract %din from 0 : (i8) -> i4
        %4 = hw.constant 9 : i4
        %5 = comb.icmp eq %3, %4 : i4
        %6 = hw.constant 0 : i1
        %7 = comb.extract %din from 4 : (i8) -> i1
        %8 = comb.extract %din from 5 : (i8) -> i1
        %9 = comb.extract %din from 6 : (i8) -> i1
        %10 = comb.extract %din from 7 : (i8) -> i1
        %11 = comb.concat %10, %9, %8, %7 : i1, i1, i1, i1
        %12 = hw.constant 1 : i4
        %13 = comb.add %11, %12 : i4
        %14 = comb.extract %13 from 0 : (i4) -> i1
        %15 = comb.extract %13 from 1 : (i4) -> i1
        %16 = comb.extract %13 from 2 : (i4) -> i1
        %17 = comb.extract %13 from 3 : (i4) -> i1
        %18 = comb.extract %din from 0 : (i8) -> i1
        %19 = comb.extract %din from 1 : (i8) -> i1
        %20 = comb.extract %din from 2 : (i8) -> i1
        %21 = comb.extract %din from 3 : (i8) -> i1
        %22 = comb.concat %21, %20, %19, %18 : i1, i1, i1, i1
        %23 = hw.constant 1 : i4
        %24 = comb.add %22, %23 : i4
        %25 = comb.extract %24 from 0 : (i4) -> i1
        %26 = comb.extract %24 from 1 : (i4) -> i1
        %27 = comb.extract %24 from 2 : (i4) -> i1
        %28 = comb.extract %24 from 3 : (i4) -> i1
        %30 = sv.reg : !hw.inout<i8>
        %29 = sv.read_inout %30 : !hw.inout<i8>
        sv.alwayscomb {
            sv.if %1 {
                %31 = comb.concat %6, %6, %6, %6, %6, %6, %6, %6 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %30, %31 : i8
            } else {
                sv.if %5 {
                    %32 = comb.concat %17, %16, %15, %14, %6, %6, %6, %6 : i1, i1, i1, i1, i1, i1, i1, i1
                    sv.bpassign %30, %32 : i8
                } else {
                    %33 = comb.concat %10, %9, %8, %7, %28, %27, %26, %25 : i1, i1, i1, i1, i1, i1, i1, i1
                    sv.bpassign %30, %33 : i8
                }
            }
        }
        hw.output %29 : i8
    }
    hw.module @seven_seg_hex(in %din: i4, out dout: i7) {
        %0 = hw.constant 64 : i7
        %1 = hw.constant 63 : i7
        %2 = hw.constant 0 : i4
        %3 = comb.icmp eq %din, %2 : i4
        %5 = hw.array_create %1, %0 : i7
        %4 = hw.array_get %5[%3] : !hw.array<2xi7>, i1
        %6 = hw.constant 6 : i7
        %7 = hw.constant 1 : i4
        %8 = comb.icmp eq %din, %7 : i4
        %10 = hw.array_create %6, %4 : i7
        %9 = hw.array_get %10[%8] : !hw.array<2xi7>, i1
        %11 = hw.constant 91 : i7
        %12 = hw.constant 2 : i4
        %13 = comb.icmp eq %din, %12 : i4
        %15 = hw.array_create %11, %9 : i7
        %14 = hw.array_get %15[%13] : !hw.array<2xi7>, i1
        %16 = hw.constant 79 : i7
        %17 = hw.constant 3 : i4
        %18 = comb.icmp eq %din, %17 : i4
        %20 = hw.array_create %16, %14 : i7
        %19 = hw.array_get %20[%18] : !hw.array<2xi7>, i1
        %21 = hw.constant 102 : i7
        %22 = hw.constant 4 : i4
        %23 = comb.icmp eq %din, %22 : i4
        %25 = hw.array_create %21, %19 : i7
        %24 = hw.array_get %25[%23] : !hw.array<2xi7>, i1
        %26 = hw.constant 109 : i7
        %27 = hw.constant 5 : i4
        %28 = comb.icmp eq %din, %27 : i4
        %30 = hw.array_create %26, %24 : i7
        %29 = hw.array_get %30[%28] : !hw.array<2xi7>, i1
        %31 = hw.constant 125 : i7
        %32 = hw.constant 6 : i4
        %33 = comb.icmp eq %din, %32 : i4
        %35 = hw.array_create %31, %29 : i7
        %34 = hw.array_get %35[%33] : !hw.array<2xi7>, i1
        %36 = hw.constant 7 : i7
        %37 = hw.constant 7 : i4
        %38 = comb.icmp eq %din, %37 : i4
        %40 = hw.array_create %36, %34 : i7
        %39 = hw.array_get %40[%38] : !hw.array<2xi7>, i1
        %41 = hw.constant 127 : i7
        %42 = hw.constant 8 : i4
        %43 = comb.icmp eq %din, %42 : i4
        %45 = hw.array_create %41, %39 : i7
        %44 = hw.array_get %45[%43] : !hw.array<2xi7>, i1
        %46 = hw.constant 111 : i7
        %47 = hw.constant 9 : i4
        %48 = comb.icmp eq %din, %47 : i4
        %50 = hw.array_create %46, %44 : i7
        %49 = hw.array_get %50[%48] : !hw.array<2xi7>, i1
        %51 = hw.constant 119 : i7
        %52 = hw.constant 10 : i4
        %53 = comb.icmp eq %din, %52 : i4
        %55 = hw.array_create %51, %49 : i7
        %54 = hw.array_get %55[%53] : !hw.array<2xi7>, i1
        %56 = hw.constant 124 : i7
        %57 = hw.constant 11 : i4
        %58 = comb.icmp eq %din, %57 : i4
        %60 = hw.array_create %56, %54 : i7
        %59 = hw.array_get %60[%58] : !hw.array<2xi7>, i1
        %61 = hw.constant 57 : i7
        %62 = hw.constant 12 : i4
        %63 = comb.icmp eq %din, %62 : i4
        %65 = hw.array_create %61, %59 : i7
        %64 = hw.array_get %65[%63] : !hw.array<2xi7>, i1
        %66 = hw.constant 94 : i7
        %67 = hw.constant 13 : i4
        %68 = comb.icmp eq %din, %67 : i4
        %70 = hw.array_create %66, %64 : i7
        %69 = hw.array_get %70[%68] : !hw.array<2xi7>, i1
        %71 = hw.constant 121 : i7
        %72 = hw.constant 14 : i4
        %73 = comb.icmp eq %din, %72 : i4
        %75 = hw.array_create %71, %69 : i7
        %74 = hw.array_get %75[%73] : !hw.array<2xi7>, i1
        %76 = hw.constant 113 : i7
        %77 = hw.constant 15 : i4
        %78 = comb.icmp eq %din, %77 : i4
        %80 = hw.array_create %76, %74 : i7
        %79 = hw.array_get %80[%78] : !hw.array<2xi7>, i1
        hw.output %79 : i7
    }
    hw.module @Counter_unq1(in %CLK: i1, out O: i10) {
        %0 = hw.constant 1 : i10
        %2 = comb.add %1, %0 : i10
        %3 = sv.reg name "Register_inst0" : !hw.inout<i10>
        sv.alwaysff(posedge %CLK) {
            sv.passign %3, %2 : i10
        }
        %4 = hw.constant 0 : i10
        sv.initial {
            sv.bpassign %3, %4 : i10
        }
        %1 = sv.read_inout %3 : !hw.inout<i10>
        hw.output %1 : i10
    }
    hw.module @seven_seg_ctrl(in %CLK: i1, in %din: i8, out dout: i8) {
        %0 = hw.instance "Counter_inst0" @Counter_unq1(CLK: %CLK: i1) -> (O: i10)
        %2 = hw.constant -1 : i10
        %1 = comb.icmp eq %0, %2 : i10
        %4 = sv.reg name "Register_inst1" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %4, %1 : i1
        }
        %5 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %4, %5 : i1
        }
        %3 = sv.read_inout %4 : !hw.inout<i1>
        %7 = comb.xor %6, %3 : i1
        %8 = sv.reg name "Register_inst2" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %8, %7 : i1
        }
        sv.initial {
            sv.bpassign %8, %5 : i1
        }
        %6 = sv.read_inout %8 : !hw.inout<i1>
        %9 = comb.extract %din from 4 : (i8) -> i4
        %10 = hw.instance "seven_seg_hex_inst0" @seven_seg_hex(din: %9: i4) -> (dout: i7)
        %12 = hw.constant -1 : i7
        %11 = comb.xor %12, %10 : i7
        %13 = hw.constant 0 : i1
        %14 = comb.extract %din from 0 : (i8) -> i4
        %15 = hw.instance "seven_seg_hex_inst1" @seven_seg_hex(din: %14: i4) -> (dout: i7)
        %16 = comb.xor %12, %15 : i7
        %17 = hw.constant 1 : i1
        %19 = comb.extract %18 from 0 : (i8) -> i7
        %20 = comb.extract %18 from 7 : (i8) -> i1
        %23 = sv.reg : !hw.inout<i7>
        %21 = sv.read_inout %23 : !hw.inout<i7>
        %24 = sv.reg : !hw.inout<i1>
        %22 = sv.read_inout %24 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %23, %19 : i7
            sv.bpassign %24, %20 : i1
            sv.if %3 {
                sv.if %6 {
                    sv.bpassign %23, %11 : i7
                    sv.bpassign %24, %13 : i1
                } else {
                    sv.bpassign %23, %16 : i7
                    sv.bpassign %24, %17 : i1
                }
            }
        }
        %25 = comb.concat %22, %21 : i1, i7
        %26 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %26, %25 : i8
        }
        %27 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %26, %27 : i8
        }
        %18 = sv.read_inout %26 : !hw.inout<i8>
        hw.output %18 : i8
    }
    hw.module @top(in %CLK: i1, in %BTN_N: i1, in %BTN1: i1, in %BTN2: i1, in %BTN3: i1, out LED1: i1, out LED2: i1, out LED3: i1, out LED4: i1, out LED5: i1, out P1A1: i1, out P1A2: i1, out P1A3: i1, out P1A4: i1, out P1A7: i1, out P1A8: i1, out P1A9: i1, out P1A10: i1) {
        %0 = comb.and %BTN1, %BTN2 : i1
        %1 = comb.and %BTN1, %BTN3 : i1
        %2 = comb.and %BTN2, %BTN3 : i1
        %4 = hw.constant -1 : i1
        %3 = comb.xor %4, %BTN_N : i1
        %5 = comb.xor %4, %BTN_N : i1
        %6 = comb.or %5, %BTN1 : i1
        %7 = comb.or %6, %BTN2 : i1
        %8 = comb.or %7, %BTN3 : i1
        %9 = comb.xor %4, %BTN_N : i1
        %10, %11 = hw.instance "Counter_inst0" @Counter(CLK: %CLK: i1) -> (O: i21, COUT: i1)
        %12 = hw.constant 1 : i1
        %15 = sv.reg : !hw.inout<i1>
        %14 = sv.read_inout %15 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %15, %13 : i1
            sv.if %BTN3 {
                sv.bpassign %15, %12 : i1
            }
        }
        %16 = hw.constant 0 : i1
        %18 = sv.reg : !hw.inout<i1>
        %17 = sv.read_inout %18 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %18, %14 : i1
            sv.if %BTN1 {
                sv.bpassign %18, %16 : i1
            }
        }
        %20 = sv.reg name "Register_inst3" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %20, %17 : i1
        }
        %21 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %20, %21 : i1
        }
        %19 = sv.read_inout %20 : !hw.inout<i1>
        %22 = comb.and %11, %19 : i1
        %24 = hw.instance "bcd8_increment_inst0" @bcd8_increment(din: %23: i8) -> (dout: i8)
        %26 = sv.reg : !hw.inout<i8>
        %25 = sv.read_inout %26 : !hw.inout<i8>
        sv.alwayscomb {
            sv.bpassign %26, %23 : i8
            sv.if %22 {
                sv.bpassign %26, %24 : i8
            }
        }
        %27 = hw.constant 0 : i8
        %28 = hw.constant 0 : i1
        %29 = hw.constant 20 : i5
        %32 = sv.reg name "Register_inst1" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %32, %30 : i8
        }
        %33 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %32, %33 : i8
        }
        %31 = sv.read_inout %32 : !hw.inout<i8>
        %36 = sv.reg : !hw.inout<i8>
        %30 = sv.read_inout %36 : !hw.inout<i8>
        %37 = sv.reg : !hw.inout<i5>
        %35 = sv.read_inout %37 : !hw.inout<i5>
        sv.alwayscomb {
            sv.bpassign %37, %34 : i5
            sv.bpassign %36, %31 : i8
            sv.if %BTN2 {
                sv.bpassign %36, %23 : i8
                sv.bpassign %37, %29 : i5
            }
        }
        %39 = sv.reg name "Register_inst2" : !hw.inout<i5>
        sv.alwaysff(posedge %CLK) {
            sv.passign %39, %35 : i5
        }
        %40 = hw.constant 0 : i5
        sv.initial {
            sv.bpassign %39, %40 : i5
        }
        %38 = sv.read_inout %39 : !hw.inout<i5>
        %41 = hw.constant 0 : i5
        %42 = comb.icmp eq %38, %41 : i5
        %43 = comb.xor %4, %42 : i1
        %44 = comb.and %11, %43 : i1
        %45 = hw.constant 1 : i5
        %46 = comb.sub %38, %45 : i5
        %48 = sv.reg : !hw.inout<i5>
        %47 = sv.read_inout %48 : !hw.inout<i5>
        sv.alwayscomb {
            sv.bpassign %48, %38 : i5
            sv.if %44 {
                sv.bpassign %48, %46 : i5
            }
        }
        %49 = hw.constant 0 : i5
        %51 = sv.reg : !hw.inout<i8>
        %50 = sv.read_inout %51 : !hw.inout<i8>
        %52 = sv.reg : !hw.inout<i1>
        %13 = sv.read_inout %52 : !hw.inout<i1>
        %53 = sv.reg : !hw.inout<i5>
        %34 = sv.read_inout %53 : !hw.inout<i5>
        sv.alwayscomb {
            sv.bpassign %51, %25 : i8
            sv.bpassign %53, %47 : i5
            sv.bpassign %52, %19 : i1
            sv.if %9 {
                sv.bpassign %51, %27 : i8
                sv.bpassign %52, %28 : i1
                sv.bpassign %53, %49 : i5
            }
        }
        %54 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %54, %50 : i8
        }
        sv.initial {
            sv.bpassign %54, %33 : i8
        }
        %23 = sv.read_inout %54 : !hw.inout<i8>
        %55 = hw.constant 0 : i5
        %56 = comb.icmp eq %38, %55 : i5
        %57 = comb.xor %4, %56 : i1
        %59 = hw.array_create %31, %23 : i8
        %58 = hw.array_get %59[%57] : !hw.array<2xi8>, i1
        %60 = hw.instance "seven_seg_ctrl_inst0" @seven_seg_ctrl(CLK: %CLK: i1, din: %58: i8) -> (dout: i8)
        %61 = comb.extract %60 from 0 : (i8) -> i1
        %62 = comb.extract %60 from 1 : (i8) -> i1
        %63 = comb.extract %60 from 2 : (i8) -> i1
        %64 = comb.extract %60 from 3 : (i8) -> i1
        %65 = comb.extract %60 from 4 : (i8) -> i1
        %66 = comb.extract %60 from 5 : (i8) -> i1
        %67 = comb.extract %60 from 6 : (i8) -> i1
        %68 = comb.extract %60 from 7 : (i8) -> i1
        hw.output %0, %1, %2, %3, %8, %61, %62, %63, %64, %65, %66, %67, %68 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
    }
}
