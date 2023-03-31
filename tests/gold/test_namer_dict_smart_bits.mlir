module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_namer_dict_smart_bits(%I0: i8, %I1: i8) -> (O: i9) {
        %0 = comb.extract %I0 from 0 : (i8) -> i1
        %1 = comb.extract %I0 from 1 : (i8) -> i1
        %2 = comb.extract %I0 from 2 : (i8) -> i1
        %3 = comb.extract %I0 from 3 : (i8) -> i1
        %4 = comb.extract %I0 from 4 : (i8) -> i1
        %5 = comb.extract %I0 from 5 : (i8) -> i1
        %6 = comb.extract %I0 from 6 : (i8) -> i1
        %7 = comb.extract %I0 from 7 : (i8) -> i1
        %8 = hw.constant 0 : i1
        %9 = comb.concat %8, %7, %6, %5, %4, %3, %2, %1, %0 : i1, i1, i1, i1, i1, i1, i1, i1, i1
        %10 = comb.extract %I1 from 0 : (i8) -> i1
        %11 = comb.extract %I1 from 1 : (i8) -> i1
        %12 = comb.extract %I1 from 2 : (i8) -> i1
        %13 = comb.extract %I1 from 3 : (i8) -> i1
        %14 = comb.extract %I1 from 4 : (i8) -> i1
        %15 = comb.extract %I1 from 5 : (i8) -> i1
        %16 = comb.extract %I1 from 6 : (i8) -> i1
        %17 = comb.extract %I1 from 7 : (i8) -> i1
        %18 = hw.constant 0 : i1
        %19 = comb.concat %18, %17, %16, %15, %14, %13, %12, %11, %10 : i1, i1, i1, i1, i1, i1, i1, i1, i1
        %20 = comb.add %9, %19 : i9
        %22 = sv.wire sym @test_namer_dict_smart_bits.x name "x" : !hw.inout<i9>
        sv.assign %22, %20 : i9
        %21 = sv.read_inout %22 : !hw.inout<i9>
        hw.output %21 : i9
    }
}
