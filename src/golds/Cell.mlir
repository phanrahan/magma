hw.module @Register(%I: i1, %CLK: i1) -> (%O: i1) {
    %0 = comb.merge %I : i1
    %2 = sv.reg {name = "reg_P1_inst0"} : !hw.inout<i1>
    sv.alwaysff(posedge %CLK) {
        sv.passign %2, %0 : i1
    }
    sv.initial {
        %3 = hw.constant 0 : i1
        sv.bpassign %2, %3 : i1
    }
    %1 = sv.read_inout %2 : !hw.inout<i1>
    %4 = comb.extract %1 from 0 : (i1) -> i1
    hw.output %4 : i1
}
hw.module @Mux2xBit(%I0: i1, %I1: i1, %S: i1) -> (%O: i1) {
    %0 = comb.merge %I0 : i1
    %1 = comb.merge %I1 : i1
    %2 = hw.array_create %1, %0 : i1
    %3 = comb.merge %S : i1
    %4 = hw.struct_create (%2, %3) : !hw.struct<data: !hw.array<2xi1>, sel: i1>
    %6 = hw.struct_extract %4["data"] : !hw.struct<data: !hw.array<2xi1>, sel: i1>
    %7 = hw.struct_extract %4["sel"] : !hw.struct<data: !hw.array<2xi1>, sel: i1>
    %5 = hw.array_get %6[%7] : !hw.array<2xi1>
    %8 = comb.extract %5 from 0 : (i1) -> i1
    hw.output %8 : i1
}
hw.module @Cell(%neighbors: i8, %running: i1, %write_enable: i1, %write_value: i1, %CLK: i1) -> (%out: i1) {
    %0 = hw.constant 0 : i1
    %1 = hw.constant 1 : i1
    %4 = hw.constant -1 : i1
    %3 = comb.xor %4, %2 : i1
    %5 = hw.constant 0 : i3
    %6 = comb.extract %neighbors from 0 : (i8) -> i1
    %7 = hw.constant 0 : i1
    %8 = hw.constant 0 : i1
    %9 = comb.concat %8, %7, %6 : (i1, i1, i1) -> (i3)
    %10 = comb.add %5, %9 : i3
    %11 = comb.extract %neighbors from 1 : (i8) -> i1
    %12 = hw.constant 0 : i1
    %13 = hw.constant 0 : i1
    %14 = comb.concat %13, %12, %11 : (i1, i1, i1) -> (i3)
    %15 = comb.add %10, %14 : i3
    %16 = comb.extract %neighbors from 2 : (i8) -> i1
    %17 = hw.constant 0 : i1
    %18 = hw.constant 0 : i1
    %19 = comb.concat %18, %17, %16 : (i1, i1, i1) -> (i3)
    %20 = comb.add %15, %19 : i3
    %21 = comb.extract %neighbors from 3 : (i8) -> i1
    %22 = hw.constant 0 : i1
    %23 = hw.constant 0 : i1
    %24 = comb.concat %23, %22, %21 : (i1, i1, i1) -> (i3)
    %25 = comb.add %20, %24 : i3
    %26 = comb.extract %neighbors from 4 : (i8) -> i1
    %27 = hw.constant 0 : i1
    %28 = hw.constant 0 : i1
    %29 = comb.concat %28, %27, %26 : (i1, i1, i1) -> (i3)
    %30 = comb.add %25, %29 : i3
    %31 = comb.extract %neighbors from 5 : (i8) -> i1
    %32 = hw.constant 0 : i1
    %33 = hw.constant 0 : i1
    %34 = comb.concat %33, %32, %31 : (i1, i1, i1) -> (i3)
    %35 = comb.add %30, %34 : i3
    %36 = comb.extract %neighbors from 6 : (i8) -> i1
    %37 = hw.constant 0 : i1
    %38 = hw.constant 0 : i1
    %39 = comb.concat %38, %37, %36 : (i1, i1, i1) -> (i3)
    %40 = comb.add %35, %39 : i3
    %41 = comb.extract %neighbors from 7 : (i8) -> i1
    %42 = hw.constant 0 : i1
    %43 = hw.constant 0 : i1
    %44 = comb.concat %43, %42, %41 : (i1, i1, i1) -> (i3)
    %45 = comb.add %40, %44 : i3
    %46 = hw.constant 3 : i3
    %47 = comb.eq %45, %46 : i1
    %48 = comb.and %3, %47 : i1
    %49 = hw.instance "Mux2xBit_inst3" @Mux2xBit(%0, %1, %48) : (i1, i1, i1) -> (i1)
    %50 = hw.constant 0 : i1
    %51 = hw.constant 1 : i1
    %52 = hw.constant 4 : i3
    %53 = comb.ult %45, %52 : i1
    %54 = hw.instance "Mux2xBit_inst1" @Mux2xBit(%50, %51, %53) : (i1, i1, i1) -> (i1)
    %55 = hw.constant 0 : i1
    %56 = hw.constant 2 : i3
    %57 = comb.ult %45, %56 : i1
    %58 = hw.instance "Mux2xBit_inst2" @Mux2xBit(%54, %55, %57) : (i1, i1, i1) -> (i1)
    %59 = hw.instance "Mux2xBit_inst4" @Mux2xBit(%49, %58, %2) : (i1, i1, i1) -> (i1)
    %60 = hw.instance "Mux2xBit_inst0" @Mux2xBit(%2, %write_value, %write_enable) : (i1, i1, i1) -> (i1)
    %62 = hw.constant -1 : i1
    %61 = comb.xor %62, %running : i1
    %63 = hw.instance "Mux2xBit_inst5" @Mux2xBit(%59, %60, %61) : (i1, i1, i1) -> (i1)
    %2 = hw.instance "Register_inst0" @Register(%63, %CLK) : (i1, i1) -> (i1)
    hw.output %2 : i1
}
