module attributes {circt.loweringOptions = "locationInfoStyle=none,disallowLocalVariables"} {
    hw.module @test_when_tuple_as_bits_resolve(%I_x_y: i1, %I_x_z_x: i8, %I_x_z_y: i1, %I_x_x: !hw.array<2xi8>, %I_y: i8, %S: i1) -> (O_x_y: i1, O_x_z_x: i8, O_x_z_y: i1, O_x_x: !hw.array<2xi8>, O_y: i8, X: i34) {
        %1 = hw.constant 0 : i1
        %0 = hw.array_get %I_x_x[%1] : !hw.array<2xi8>, i1
        %3 = hw.constant 1 : i1
        %2 = hw.array_get %I_x_x[%3] : !hw.array<2xi8>, i1
        %6 = hw.array_create %I_x_z_x, %I_x_z_x : i8
        %4 = hw.array_get %6[%S] : !hw.array<2xi8>, i1
        %7 = hw.array_create %I_x_z_y, %I_x_z_y : i1
        %5 = hw.array_get %7[%S] : !hw.array<2xi1>, i1
        %14 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i8>
        %8 = sv.read_inout %14 : !hw.inout<i8>
        %15 = sv.reg name "_WHEN_WIRE_1" : !hw.inout<i8>
        %9 = sv.read_inout %15 : !hw.inout<i8>
        %16 = sv.reg name "_WHEN_WIRE_2" : !hw.inout<i1>
        %10 = sv.read_inout %16 : !hw.inout<i1>
        %17 = sv.reg name "_WHEN_WIRE_3" : !hw.inout<i8>
        %11 = sv.read_inout %17 : !hw.inout<i8>
        %18 = sv.reg name "_WHEN_WIRE_4" : !hw.inout<i1>
        %12 = sv.read_inout %18 : !hw.inout<i1>
        %19 = sv.reg name "_WHEN_WIRE_5" : !hw.inout<i8>
        %13 = sv.read_inout %19 : !hw.inout<i8>
        sv.alwayscomb {
            %28 = comb.concat %27, %26, %25, %24, %23, %22, %21, %20 : i1, i1, i1, i1, i1, i1, i1, i1
            sv.bpassign %19, %28 : i8
            sv.if %S {
                sv.bpassign %16, %I_x_y : i1
                sv.bpassign %18, %5 : i1
                %53 = comb.concat %36, %35, %34, %33, %32, %31, %30, %29 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %17, %53 : i8
                %54 = comb.concat %44, %43, %42, %41, %40, %39, %38, %37 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %14, %54 : i8
                %55 = comb.concat %52, %51, %50, %49, %48, %47, %46, %45 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %15, %55 : i8
            } else {
                sv.bpassign %16, %I_x_y : i1
                sv.bpassign %18, %I_x_z_y : i1
                %64 = comb.concat %63, %62, %61, %60, %59, %58, %57, %56 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %17, %64 : i8
                %65 = comb.concat %44, %43, %42, %41, %40, %39, %38, %37 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %14, %65 : i8
                %66 = comb.concat %52, %51, %50, %49, %48, %47, %46, %45 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %15, %66 : i8
                %67 = comb.concat %27, %26, %25, %24, %23, %22, %21, %20 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %19, %67 : i8
            }
        }
        %20 = comb.extract %I_y from 0 : (i8) -> i1
        %21 = comb.extract %I_y from 1 : (i8) -> i1
        %22 = comb.extract %I_y from 2 : (i8) -> i1
        %23 = comb.extract %I_y from 3 : (i8) -> i1
        %24 = comb.extract %I_y from 4 : (i8) -> i1
        %25 = comb.extract %I_y from 5 : (i8) -> i1
        %26 = comb.extract %I_y from 6 : (i8) -> i1
        %27 = comb.extract %I_y from 7 : (i8) -> i1
        %29 = comb.extract %4 from 0 : (i8) -> i1
        %30 = comb.extract %4 from 1 : (i8) -> i1
        %31 = comb.extract %4 from 2 : (i8) -> i1
        %32 = comb.extract %4 from 3 : (i8) -> i1
        %33 = comb.extract %4 from 4 : (i8) -> i1
        %34 = comb.extract %4 from 5 : (i8) -> i1
        %35 = comb.extract %4 from 6 : (i8) -> i1
        %36 = comb.extract %4 from 7 : (i8) -> i1
        %37 = comb.extract %0 from 0 : (i8) -> i1
        %38 = comb.extract %0 from 1 : (i8) -> i1
        %39 = comb.extract %0 from 2 : (i8) -> i1
        %40 = comb.extract %0 from 3 : (i8) -> i1
        %41 = comb.extract %0 from 4 : (i8) -> i1
        %42 = comb.extract %0 from 5 : (i8) -> i1
        %43 = comb.extract %0 from 6 : (i8) -> i1
        %44 = comb.extract %0 from 7 : (i8) -> i1
        %45 = comb.extract %2 from 0 : (i8) -> i1
        %46 = comb.extract %2 from 1 : (i8) -> i1
        %47 = comb.extract %2 from 2 : (i8) -> i1
        %48 = comb.extract %2 from 3 : (i8) -> i1
        %49 = comb.extract %2 from 4 : (i8) -> i1
        %50 = comb.extract %2 from 5 : (i8) -> i1
        %51 = comb.extract %2 from 6 : (i8) -> i1
        %52 = comb.extract %2 from 7 : (i8) -> i1
        %56 = comb.extract %I_x_z_x from 0 : (i8) -> i1
        %57 = comb.extract %I_x_z_x from 1 : (i8) -> i1
        %58 = comb.extract %I_x_z_x from 2 : (i8) -> i1
        %59 = comb.extract %I_x_z_x from 3 : (i8) -> i1
        %60 = comb.extract %I_x_z_x from 4 : (i8) -> i1
        %61 = comb.extract %I_x_z_x from 5 : (i8) -> i1
        %62 = comb.extract %I_x_z_x from 6 : (i8) -> i1
        %63 = comb.extract %I_x_z_x from 7 : (i8) -> i1
        %68 = hw.array_create %9, %8 : i8
        %69 = comb.extract %11 from 0 : (i8) -> i1
        %70 = comb.extract %11 from 1 : (i8) -> i1
        %71 = comb.extract %11 from 2 : (i8) -> i1
        %72 = comb.extract %11 from 3 : (i8) -> i1
        %73 = comb.extract %11 from 4 : (i8) -> i1
        %74 = comb.extract %11 from 5 : (i8) -> i1
        %75 = comb.extract %11 from 6 : (i8) -> i1
        %76 = comb.extract %11 from 7 : (i8) -> i1
        %77 = comb.extract %8 from 0 : (i8) -> i1
        %78 = comb.extract %8 from 1 : (i8) -> i1
        %79 = comb.extract %8 from 2 : (i8) -> i1
        %80 = comb.extract %8 from 3 : (i8) -> i1
        %81 = comb.extract %8 from 4 : (i8) -> i1
        %82 = comb.extract %8 from 5 : (i8) -> i1
        %83 = comb.extract %8 from 6 : (i8) -> i1
        %84 = comb.extract %8 from 7 : (i8) -> i1
        %85 = comb.extract %9 from 0 : (i8) -> i1
        %86 = comb.extract %9 from 1 : (i8) -> i1
        %87 = comb.extract %9 from 2 : (i8) -> i1
        %88 = comb.extract %9 from 3 : (i8) -> i1
        %89 = comb.extract %9 from 4 : (i8) -> i1
        %90 = comb.extract %9 from 5 : (i8) -> i1
        %91 = comb.extract %9 from 6 : (i8) -> i1
        %92 = comb.extract %9 from 7 : (i8) -> i1
        %93 = comb.extract %13 from 0 : (i8) -> i1
        %94 = comb.extract %13 from 1 : (i8) -> i1
        %95 = comb.extract %13 from 2 : (i8) -> i1
        %96 = comb.extract %13 from 3 : (i8) -> i1
        %97 = comb.extract %13 from 4 : (i8) -> i1
        %98 = comb.extract %13 from 5 : (i8) -> i1
        %99 = comb.extract %13 from 6 : (i8) -> i1
        %100 = comb.extract %13 from 7 : (i8) -> i1
        %101 = comb.concat %100, %99, %98, %97, %96, %95, %94, %93, %92, %91, %90, %89, %88, %87, %86, %85, %84, %83, %82, %81, %80, %79, %78, %77, %12, %76, %75, %74, %73, %72, %71, %70, %69, %10 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %10, %I_x_y) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %12, %5) : i1, i1, i1
        %102 = comb.extract %4 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %69, %102) : i1, i1, i1
        %103 = comb.extract %4 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %70, %103) : i1, i1, i1
        %104 = comb.extract %4 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %71, %104) : i1, i1, i1
        %105 = comb.extract %4 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %72, %105) : i1, i1, i1
        %106 = comb.extract %4 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %73, %106) : i1, i1, i1
        %107 = comb.extract %4 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %74, %107) : i1, i1, i1
        %108 = comb.extract %4 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %75, %108) : i1, i1, i1
        %109 = comb.extract %4 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_9: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %76, %109) : i1, i1, i1
        %110 = comb.extract %0 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_10: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %77, %110) : i1, i1, i1
        %111 = comb.extract %0 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_11: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %78, %111) : i1, i1, i1
        %112 = comb.extract %0 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_12: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %79, %112) : i1, i1, i1
        %113 = comb.extract %0 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_13: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %80, %113) : i1, i1, i1
        %114 = comb.extract %0 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_14: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %81, %114) : i1, i1, i1
        %115 = comb.extract %0 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_15: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %82, %115) : i1, i1, i1
        %116 = comb.extract %0 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_16: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %83, %116) : i1, i1, i1
        %117 = comb.extract %0 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_17: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %84, %117) : i1, i1, i1
        %118 = comb.extract %2 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_18: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %85, %118) : i1, i1, i1
        %119 = comb.extract %2 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_19: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %86, %119) : i1, i1, i1
        %120 = comb.extract %2 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_20: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %87, %120) : i1, i1, i1
        %121 = comb.extract %2 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_21: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %88, %121) : i1, i1, i1
        %122 = comb.extract %2 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_22: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %89, %122) : i1, i1, i1
        %123 = comb.extract %2 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_23: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %90, %123) : i1, i1, i1
        %124 = comb.extract %2 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_24: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %91, %124) : i1, i1, i1
        %125 = comb.extract %2 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_25: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %92, %125) : i1, i1, i1
        %127 = hw.constant -1 : i1
        %126 = comb.xor %127, %S : i1
        sv.verbatim "WHEN_ASSERT_26: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %10, %I_x_y) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_27: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %12, %I_x_z_y) : i1, i1, i1
        %128 = comb.extract %I_x_z_x from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_28: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %69, %128) : i1, i1, i1
        %129 = comb.extract %I_x_z_x from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_29: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %70, %129) : i1, i1, i1
        %130 = comb.extract %I_x_z_x from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_30: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %71, %130) : i1, i1, i1
        %131 = comb.extract %I_x_z_x from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_31: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %72, %131) : i1, i1, i1
        %132 = comb.extract %I_x_z_x from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_32: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %73, %132) : i1, i1, i1
        %133 = comb.extract %I_x_z_x from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_33: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %74, %133) : i1, i1, i1
        %134 = comb.extract %I_x_z_x from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_34: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %75, %134) : i1, i1, i1
        %135 = comb.extract %I_x_z_x from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_35: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %76, %135) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_36: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %77, %110) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_37: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %78, %111) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_38: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %79, %112) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_39: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %80, %113) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_40: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %81, %114) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_41: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %82, %115) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_42: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %83, %116) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_43: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %84, %117) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_44: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %85, %118) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_45: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %86, %119) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_46: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %87, %120) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_47: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %88, %121) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_48: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %89, %122) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_49: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %90, %123) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_50: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %91, %124) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_51: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %92, %125) : i1, i1, i1
        %136 = comb.extract %I_y from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_52: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %93, %136) : i1, i1, i1
        %137 = comb.extract %I_y from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_53: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %94, %137) : i1, i1, i1
        %138 = comb.extract %I_y from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_54: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %95, %138) : i1, i1, i1
        %139 = comb.extract %I_y from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_55: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %96, %139) : i1, i1, i1
        %140 = comb.extract %I_y from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_56: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %97, %140) : i1, i1, i1
        %141 = comb.extract %I_y from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_57: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %98, %141) : i1, i1, i1
        %142 = comb.extract %I_y from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_58: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %99, %142) : i1, i1, i1
        %143 = comb.extract %I_y from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_59: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%126, %100, %143) : i1, i1, i1
        %144 = comb.xor %127, %126 : i1
        sv.verbatim "WHEN_ASSERT_60: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%144, %93, %136) : i1, i1, i1
        %145 = comb.xor %127, %126 : i1
        sv.verbatim "WHEN_ASSERT_61: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%145, %94, %137) : i1, i1, i1
        %146 = comb.xor %127, %126 : i1
        sv.verbatim "WHEN_ASSERT_62: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%146, %95, %138) : i1, i1, i1
        %147 = comb.xor %127, %126 : i1
        sv.verbatim "WHEN_ASSERT_63: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%147, %96, %139) : i1, i1, i1
        %148 = comb.xor %127, %126 : i1
        sv.verbatim "WHEN_ASSERT_64: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%148, %97, %140) : i1, i1, i1
        %149 = comb.xor %127, %126 : i1
        sv.verbatim "WHEN_ASSERT_65: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%149, %98, %141) : i1, i1, i1
        %150 = comb.xor %127, %126 : i1
        sv.verbatim "WHEN_ASSERT_66: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%150, %99, %142) : i1, i1, i1
        %151 = comb.xor %127, %126 : i1
        sv.verbatim "WHEN_ASSERT_67: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%151, %100, %143) : i1, i1, i1
        hw.output %10, %11, %12, %68, %13, %101 : i1, i8, i1, !hw.array<2xi8>, i8, i34
    }
}
