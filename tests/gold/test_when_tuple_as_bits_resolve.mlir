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
        %14 = sv.reg : !hw.inout<i8>
        %8 = sv.read_inout %14 : !hw.inout<i8>
        %15 = sv.reg : !hw.inout<i8>
        %9 = sv.read_inout %15 : !hw.inout<i8>
        %16 = sv.reg : !hw.inout<i1>
        %10 = sv.read_inout %16 : !hw.inout<i1>
        %17 = sv.reg : !hw.inout<i8>
        %11 = sv.read_inout %17 : !hw.inout<i8>
        %18 = sv.reg : !hw.inout<i1>
        %12 = sv.read_inout %18 : !hw.inout<i1>
        %19 = sv.reg : !hw.inout<i8>
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
        %69 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %69, %10 : i1
        %68 = sv.read_inout %69 : !hw.inout<i1>
        %70 = comb.extract %11 from 0 : (i8) -> i1
        %72 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %72, %70 : i1
        %71 = sv.read_inout %72 : !hw.inout<i1>
        %73 = comb.extract %11 from 1 : (i8) -> i1
        %75 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i1>
        sv.assign %75, %73 : i1
        %74 = sv.read_inout %75 : !hw.inout<i1>
        %76 = comb.extract %11 from 2 : (i8) -> i1
        %78 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_4 name "_WHEN_ASSERT_4" : !hw.inout<i1>
        sv.assign %78, %76 : i1
        %77 = sv.read_inout %78 : !hw.inout<i1>
        %79 = comb.extract %11 from 3 : (i8) -> i1
        %81 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_5 name "_WHEN_ASSERT_5" : !hw.inout<i1>
        sv.assign %81, %79 : i1
        %80 = sv.read_inout %81 : !hw.inout<i1>
        %82 = comb.extract %11 from 4 : (i8) -> i1
        %84 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_6 name "_WHEN_ASSERT_6" : !hw.inout<i1>
        sv.assign %84, %82 : i1
        %83 = sv.read_inout %84 : !hw.inout<i1>
        %85 = comb.extract %11 from 5 : (i8) -> i1
        %87 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_7 name "_WHEN_ASSERT_7" : !hw.inout<i1>
        sv.assign %87, %85 : i1
        %86 = sv.read_inout %87 : !hw.inout<i1>
        %88 = comb.extract %11 from 6 : (i8) -> i1
        %90 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_8 name "_WHEN_ASSERT_8" : !hw.inout<i1>
        sv.assign %90, %88 : i1
        %89 = sv.read_inout %90 : !hw.inout<i1>
        %91 = comb.extract %11 from 7 : (i8) -> i1
        %93 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_9 name "_WHEN_ASSERT_9" : !hw.inout<i1>
        sv.assign %93, %91 : i1
        %92 = sv.read_inout %93 : !hw.inout<i1>
        %94 = comb.concat %92, %89, %86, %83, %80, %77, %74, %71 : i1, i1, i1, i1, i1, i1, i1, i1
        %96 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %96, %12 : i1
        %95 = sv.read_inout %96 : !hw.inout<i1>
        %97 = comb.extract %8 from 0 : (i8) -> i1
        %99 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_10 name "_WHEN_ASSERT_10" : !hw.inout<i1>
        sv.assign %99, %97 : i1
        %98 = sv.read_inout %99 : !hw.inout<i1>
        %100 = comb.extract %8 from 1 : (i8) -> i1
        %102 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_11 name "_WHEN_ASSERT_11" : !hw.inout<i1>
        sv.assign %102, %100 : i1
        %101 = sv.read_inout %102 : !hw.inout<i1>
        %103 = comb.extract %8 from 2 : (i8) -> i1
        %105 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_12 name "_WHEN_ASSERT_12" : !hw.inout<i1>
        sv.assign %105, %103 : i1
        %104 = sv.read_inout %105 : !hw.inout<i1>
        %106 = comb.extract %8 from 3 : (i8) -> i1
        %108 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_13 name "_WHEN_ASSERT_13" : !hw.inout<i1>
        sv.assign %108, %106 : i1
        %107 = sv.read_inout %108 : !hw.inout<i1>
        %109 = comb.extract %8 from 4 : (i8) -> i1
        %111 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_14 name "_WHEN_ASSERT_14" : !hw.inout<i1>
        sv.assign %111, %109 : i1
        %110 = sv.read_inout %111 : !hw.inout<i1>
        %112 = comb.extract %8 from 5 : (i8) -> i1
        %114 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_15 name "_WHEN_ASSERT_15" : !hw.inout<i1>
        sv.assign %114, %112 : i1
        %113 = sv.read_inout %114 : !hw.inout<i1>
        %115 = comb.extract %8 from 6 : (i8) -> i1
        %117 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_16 name "_WHEN_ASSERT_16" : !hw.inout<i1>
        sv.assign %117, %115 : i1
        %116 = sv.read_inout %117 : !hw.inout<i1>
        %118 = comb.extract %8 from 7 : (i8) -> i1
        %120 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_17 name "_WHEN_ASSERT_17" : !hw.inout<i1>
        sv.assign %120, %118 : i1
        %119 = sv.read_inout %120 : !hw.inout<i1>
        %121 = comb.concat %119, %116, %113, %110, %107, %104, %101, %98 : i1, i1, i1, i1, i1, i1, i1, i1
        %122 = comb.extract %9 from 0 : (i8) -> i1
        %124 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_18 name "_WHEN_ASSERT_18" : !hw.inout<i1>
        sv.assign %124, %122 : i1
        %123 = sv.read_inout %124 : !hw.inout<i1>
        %125 = comb.extract %9 from 1 : (i8) -> i1
        %127 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_19 name "_WHEN_ASSERT_19" : !hw.inout<i1>
        sv.assign %127, %125 : i1
        %126 = sv.read_inout %127 : !hw.inout<i1>
        %128 = comb.extract %9 from 2 : (i8) -> i1
        %130 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_20 name "_WHEN_ASSERT_20" : !hw.inout<i1>
        sv.assign %130, %128 : i1
        %129 = sv.read_inout %130 : !hw.inout<i1>
        %131 = comb.extract %9 from 3 : (i8) -> i1
        %133 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_21 name "_WHEN_ASSERT_21" : !hw.inout<i1>
        sv.assign %133, %131 : i1
        %132 = sv.read_inout %133 : !hw.inout<i1>
        %134 = comb.extract %9 from 4 : (i8) -> i1
        %136 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_22 name "_WHEN_ASSERT_22" : !hw.inout<i1>
        sv.assign %136, %134 : i1
        %135 = sv.read_inout %136 : !hw.inout<i1>
        %137 = comb.extract %9 from 5 : (i8) -> i1
        %139 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_23 name "_WHEN_ASSERT_23" : !hw.inout<i1>
        sv.assign %139, %137 : i1
        %138 = sv.read_inout %139 : !hw.inout<i1>
        %140 = comb.extract %9 from 6 : (i8) -> i1
        %142 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_24 name "_WHEN_ASSERT_24" : !hw.inout<i1>
        sv.assign %142, %140 : i1
        %141 = sv.read_inout %142 : !hw.inout<i1>
        %143 = comb.extract %9 from 7 : (i8) -> i1
        %145 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_25 name "_WHEN_ASSERT_25" : !hw.inout<i1>
        sv.assign %145, %143 : i1
        %144 = sv.read_inout %145 : !hw.inout<i1>
        %146 = comb.concat %144, %141, %138, %135, %132, %129, %126, %123 : i1, i1, i1, i1, i1, i1, i1, i1
        %147 = hw.array_create %146, %121 : i8
        %148 = comb.extract %13 from 0 : (i8) -> i1
        %150 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_26 name "_WHEN_ASSERT_26" : !hw.inout<i1>
        sv.assign %150, %148 : i1
        %149 = sv.read_inout %150 : !hw.inout<i1>
        %151 = comb.extract %13 from 1 : (i8) -> i1
        %153 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_27 name "_WHEN_ASSERT_27" : !hw.inout<i1>
        sv.assign %153, %151 : i1
        %152 = sv.read_inout %153 : !hw.inout<i1>
        %154 = comb.extract %13 from 2 : (i8) -> i1
        %156 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_28 name "_WHEN_ASSERT_28" : !hw.inout<i1>
        sv.assign %156, %154 : i1
        %155 = sv.read_inout %156 : !hw.inout<i1>
        %157 = comb.extract %13 from 3 : (i8) -> i1
        %159 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_29 name "_WHEN_ASSERT_29" : !hw.inout<i1>
        sv.assign %159, %157 : i1
        %158 = sv.read_inout %159 : !hw.inout<i1>
        %160 = comb.extract %13 from 4 : (i8) -> i1
        %162 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_30 name "_WHEN_ASSERT_30" : !hw.inout<i1>
        sv.assign %162, %160 : i1
        %161 = sv.read_inout %162 : !hw.inout<i1>
        %163 = comb.extract %13 from 5 : (i8) -> i1
        %165 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_31 name "_WHEN_ASSERT_31" : !hw.inout<i1>
        sv.assign %165, %163 : i1
        %164 = sv.read_inout %165 : !hw.inout<i1>
        %166 = comb.extract %13 from 6 : (i8) -> i1
        %168 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_32 name "_WHEN_ASSERT_32" : !hw.inout<i1>
        sv.assign %168, %166 : i1
        %167 = sv.read_inout %168 : !hw.inout<i1>
        %169 = comb.extract %13 from 7 : (i8) -> i1
        %171 = sv.wire sym @test_when_tuple_as_bits_resolve._WHEN_ASSERT_33 name "_WHEN_ASSERT_33" : !hw.inout<i1>
        sv.assign %171, %169 : i1
        %170 = sv.read_inout %171 : !hw.inout<i1>
        %172 = comb.concat %170, %167, %164, %161, %158, %155, %152, %149 : i1, i1, i1, i1, i1, i1, i1, i1
        %173 = comb.concat %170, %167, %164, %161, %158, %155, %152, %149, %144, %141, %138, %135, %132, %129, %126, %123, %119, %116, %113, %110, %107, %104, %101, %98, %95, %92, %89, %86, %83, %80, %77, %74, %71, %68 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %68, %I_x_y) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %95, %5) : i1, i1, i1
        %174 = comb.extract %4 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %71, %174) : i1, i1, i1
        %175 = comb.extract %4 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %74, %175) : i1, i1, i1
        %176 = comb.extract %4 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %77, %176) : i1, i1, i1
        %177 = comb.extract %4 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %80, %177) : i1, i1, i1
        %178 = comb.extract %4 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %83, %178) : i1, i1, i1
        %179 = comb.extract %4 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %86, %179) : i1, i1, i1
        %180 = comb.extract %4 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %89, %180) : i1, i1, i1
        %181 = comb.extract %4 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_9: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %92, %181) : i1, i1, i1
        %182 = comb.extract %0 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_10: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %98, %182) : i1, i1, i1
        %183 = comb.extract %0 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_11: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %101, %183) : i1, i1, i1
        %184 = comb.extract %0 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_12: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %104, %184) : i1, i1, i1
        %185 = comb.extract %0 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_13: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %107, %185) : i1, i1, i1
        %186 = comb.extract %0 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_14: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %110, %186) : i1, i1, i1
        %187 = comb.extract %0 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_15: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %113, %187) : i1, i1, i1
        %188 = comb.extract %0 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_16: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %116, %188) : i1, i1, i1
        %189 = comb.extract %0 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_17: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %119, %189) : i1, i1, i1
        %190 = comb.extract %2 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_18: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %123, %190) : i1, i1, i1
        %191 = comb.extract %2 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_19: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %126, %191) : i1, i1, i1
        %192 = comb.extract %2 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_20: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %129, %192) : i1, i1, i1
        %193 = comb.extract %2 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_21: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %132, %193) : i1, i1, i1
        %194 = comb.extract %2 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_22: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %135, %194) : i1, i1, i1
        %195 = comb.extract %2 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_23: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %138, %195) : i1, i1, i1
        %196 = comb.extract %2 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_24: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %141, %196) : i1, i1, i1
        %197 = comb.extract %2 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_25: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %144, %197) : i1, i1, i1
        %199 = hw.constant -1 : i1
        %198 = comb.xor %199, %S : i1
        sv.verbatim "WHEN_ASSERT_26: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %68, %I_x_y) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_27: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %95, %I_x_z_y) : i1, i1, i1
        %200 = comb.extract %I_x_z_x from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_28: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %71, %200) : i1, i1, i1
        %201 = comb.extract %I_x_z_x from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_29: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %74, %201) : i1, i1, i1
        %202 = comb.extract %I_x_z_x from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_30: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %77, %202) : i1, i1, i1
        %203 = comb.extract %I_x_z_x from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_31: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %80, %203) : i1, i1, i1
        %204 = comb.extract %I_x_z_x from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_32: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %83, %204) : i1, i1, i1
        %205 = comb.extract %I_x_z_x from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_33: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %86, %205) : i1, i1, i1
        %206 = comb.extract %I_x_z_x from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_34: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %89, %206) : i1, i1, i1
        %207 = comb.extract %I_x_z_x from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_35: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %92, %207) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_36: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %98, %182) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_37: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %101, %183) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_38: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %104, %184) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_39: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %107, %185) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_40: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %110, %186) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_41: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %113, %187) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_42: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %116, %188) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_43: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %119, %189) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_44: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %123, %190) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_45: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %126, %191) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_46: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %129, %192) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_47: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %132, %193) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_48: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %135, %194) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_49: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %138, %195) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_50: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %141, %196) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_51: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %144, %197) : i1, i1, i1
        %208 = comb.extract %I_y from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_52: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %149, %208) : i1, i1, i1
        %209 = comb.extract %I_y from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_53: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %152, %209) : i1, i1, i1
        %210 = comb.extract %I_y from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_54: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %155, %210) : i1, i1, i1
        %211 = comb.extract %I_y from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_55: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %158, %211) : i1, i1, i1
        %212 = comb.extract %I_y from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_56: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %161, %212) : i1, i1, i1
        %213 = comb.extract %I_y from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_57: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %164, %213) : i1, i1, i1
        %214 = comb.extract %I_y from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_58: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %167, %214) : i1, i1, i1
        %215 = comb.extract %I_y from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_59: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%198, %170, %215) : i1, i1, i1
        %216 = comb.xor %199, %198 : i1
        sv.verbatim "WHEN_ASSERT_60: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%216, %149, %208) : i1, i1, i1
        %217 = comb.xor %199, %198 : i1
        sv.verbatim "WHEN_ASSERT_61: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%217, %152, %209) : i1, i1, i1
        %218 = comb.xor %199, %198 : i1
        sv.verbatim "WHEN_ASSERT_62: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%218, %155, %210) : i1, i1, i1
        %219 = comb.xor %199, %198 : i1
        sv.verbatim "WHEN_ASSERT_63: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%219, %158, %211) : i1, i1, i1
        %220 = comb.xor %199, %198 : i1
        sv.verbatim "WHEN_ASSERT_64: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%220, %161, %212) : i1, i1, i1
        %221 = comb.xor %199, %198 : i1
        sv.verbatim "WHEN_ASSERT_65: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%221, %164, %213) : i1, i1, i1
        %222 = comb.xor %199, %198 : i1
        sv.verbatim "WHEN_ASSERT_66: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%222, %167, %214) : i1, i1, i1
        %223 = comb.xor %199, %198 : i1
        sv.verbatim "WHEN_ASSERT_67: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%223, %170, %215) : i1, i1, i1
        hw.output %68, %94, %95, %147, %172, %173 : i1, i8, i1, !hw.array<2xi8>, i8, i34
    }
}
