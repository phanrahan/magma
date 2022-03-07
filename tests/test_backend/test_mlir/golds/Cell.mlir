hw.module @Cell(%neighbors: i8, %running: i1, %write_enable: i1, %write_value: i1, %CLK: i1) -> (out: i1) {
    %0 = hw.constant 0 : i1
    %1 = hw.constant 1 : i1
    %4 = hw.constant -1 : i1
    %3 = comb.xor %4, %2 : i1
    %5 = hw.constant 0 : i3
    %6 = comb.extract %neighbors from 0 : (i8) -> i1
    %7 = hw.constant 0 : i1
    %8 = hw.constant 0 : i1
    %9 = comb.concat %8, %7, %6 : i1, i1, i1
    %10 = comb.add %5, %9 : i3
    %11 = comb.extract %neighbors from 1 : (i8) -> i1
    %12 = hw.constant 0 : i1
    %13 = hw.constant 0 : i1
    %14 = comb.concat %13, %12, %11 : i1, i1, i1
    %15 = comb.add %10, %14 : i3
    %16 = comb.extract %neighbors from 2 : (i8) -> i1
    %17 = hw.constant 0 : i1
    %18 = hw.constant 0 : i1
    %19 = comb.concat %18, %17, %16 : i1, i1, i1
    %20 = comb.add %15, %19 : i3
    %21 = comb.extract %neighbors from 3 : (i8) -> i1
    %22 = hw.constant 0 : i1
    %23 = hw.constant 0 : i1
    %24 = comb.concat %23, %22, %21 : i1, i1, i1
    %25 = comb.add %20, %24 : i3
    %26 = comb.extract %neighbors from 4 : (i8) -> i1
    %27 = hw.constant 0 : i1
    %28 = hw.constant 0 : i1
    %29 = comb.concat %28, %27, %26 : i1, i1, i1
    %30 = comb.add %25, %29 : i3
    %31 = comb.extract %neighbors from 5 : (i8) -> i1
    %32 = hw.constant 0 : i1
    %33 = hw.constant 0 : i1
    %34 = comb.concat %33, %32, %31 : i1, i1, i1
    %35 = comb.add %30, %34 : i3
    %36 = comb.extract %neighbors from 6 : (i8) -> i1
    %37 = hw.constant 0 : i1
    %38 = hw.constant 0 : i1
    %39 = comb.concat %38, %37, %36 : i1, i1, i1
    %40 = comb.add %35, %39 : i3
    %41 = comb.extract %neighbors from 7 : (i8) -> i1
    %42 = hw.constant 0 : i1
    %43 = hw.constant 0 : i1
    %44 = comb.concat %43, %42, %41 : i1, i1, i1
    %45 = comb.add %40, %44 : i3
    %46 = hw.constant 3 : i3
    %47 = comb.icmp eq %45, %46 : i3
    %48 = comb.and %3, %47 : i1
    %50 = hw.array_create %0, %1 : i1
    %49 = hw.array_get %50[%48] : !hw.array<2xi1>
    %51 = hw.constant 0 : i1
    %52 = hw.constant 1 : i1
    %53 = hw.constant 4 : i3
    %54 = comb.icmp ult %45, %53 : i3
    %56 = hw.array_create %51, %52 : i1
    %55 = hw.array_get %56[%54] : !hw.array<2xi1>
    %57 = hw.constant 0 : i1
    %58 = hw.constant 2 : i3
    %59 = comb.icmp ult %45, %58 : i3
    %61 = hw.array_create %55, %57 : i1
    %60 = hw.array_get %61[%59] : !hw.array<2xi1>
    %63 = hw.array_create %49, %60 : i1
    %62 = hw.array_get %63[%2] : !hw.array<2xi1>
    %65 = hw.array_create %2, %write_value : i1
    %64 = hw.array_get %65[%write_enable] : !hw.array<2xi1>
    %66 = comb.xor %4, %running : i1
    %68 = hw.array_create %62, %64 : i1
    %67 = hw.array_get %68[%66] : !hw.array<2xi1>
    %69 = sv.reg {name = "Register_inst0"} : !hw.inout<i1>
    sv.alwaysff(posedge %CLK) {
        sv.passign %69, %67 : i1
    }
    %70 = hw.constant 0 : i1
    sv.initial {
        sv.bpassign %69, %70 : i1
    }
    %2 = sv.read_inout %69 : !hw.inout<i1>
    hw.output %2 : i1
}
