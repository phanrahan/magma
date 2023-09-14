module attributes {circt.loweringOptions = "locationInfoStyle=none,disallowLocalVariables"} {
    hw.module @test_when_tuple_as_bits_resolve_False(%I: !hw.struct<x: !hw.struct<y: i1, z: !hw.struct<x: i8, y: i1>, x: !hw.array<2xi8>>, y: i8>, %S: i1) -> (O: !hw.struct<x: !hw.struct<y: i1, z: !hw.struct<x: i8, y: i1>, x: !hw.array<2xi8>>, y: i8>, X: i34) {
        %0 = hw.struct_extract %I["x"] : !hw.struct<x: !hw.struct<y: i1, z: !hw.struct<x: i8, y: i1>, x: !hw.array<2xi8>>, y: i8>
        %1 = hw.struct_extract %0["x"] : !hw.struct<y: i1, z: !hw.struct<x: i8, y: i1>, x: !hw.array<2xi8>>
        %3 = hw.constant 0 : i1
        %2 = hw.array_get %1[%3] : !hw.array<2xi8>, i1
        %5 = hw.constant 1 : i1
        %4 = hw.array_get %1[%5] : !hw.array<2xi8>, i1
        %6 = hw.struct_extract %0["y"] : !hw.struct<y: i1, z: !hw.struct<x: i8, y: i1>, x: !hw.array<2xi8>>
        %7 = hw.struct_extract %0["z"] : !hw.struct<y: i1, z: !hw.struct<x: i8, y: i1>, x: !hw.array<2xi8>>
        %9 = hw.array_create %7, %7 : !hw.struct<x: i8, y: i1>
        %8 = hw.array_get %9[%S] : !hw.array<2x!hw.struct<x: i8, y: i1>>, i1
        %10 = hw.struct_extract %I["y"] : !hw.struct<x: !hw.struct<y: i1, z: !hw.struct<x: i8, y: i1>, x: !hw.array<2xi8>>, y: i8>
        %16 = sv.reg : !hw.inout<i8>
        %11 = sv.read_inout %16 : !hw.inout<i8>
        %17 = sv.reg : !hw.inout<i8>
        %12 = sv.read_inout %17 : !hw.inout<i8>
        %18 = sv.reg : !hw.inout<i1>
        %13 = sv.read_inout %18 : !hw.inout<i1>
        %19 = sv.reg : !hw.inout<!hw.struct<x: i8, y: i1>>
        %14 = sv.read_inout %19 : !hw.inout<!hw.struct<x: i8, y: i1>>
        %20 = sv.reg : !hw.inout<i8>
        %15 = sv.read_inout %20 : !hw.inout<i8>
        sv.alwayscomb {
            %29 = comb.concat %28, %27, %26, %25, %24, %23, %22, %21 : i1, i1, i1, i1, i1, i1, i1, i1
            sv.bpassign %20, %29 : i8
            sv.if %S {
                sv.bpassign %18, %6 : i1
                %57 = comb.concat %39, %38, %37, %36, %35, %34, %33, %32 : i1, i1, i1, i1, i1, i1, i1, i1
                %56 = hw.struct_create (%57, %30) : !hw.struct<x: i8, y: i1>
                sv.bpassign %19, %56 : !hw.struct<x: i8, y: i1>
                %58 = comb.concat %47, %46, %45, %44, %43, %42, %41, %40 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %16, %58 : i8
                %59 = comb.concat %55, %54, %53, %52, %51, %50, %49, %48 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %17, %59 : i8
            } else {
                sv.bpassign %18, %6 : i1
                %71 = comb.concat %69, %68, %67, %66, %65, %64, %63, %62 : i1, i1, i1, i1, i1, i1, i1, i1
                %70 = hw.struct_create (%71, %60) : !hw.struct<x: i8, y: i1>
                sv.bpassign %19, %70 : !hw.struct<x: i8, y: i1>
                %72 = comb.concat %47, %46, %45, %44, %43, %42, %41, %40 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %16, %72 : i8
                %73 = comb.concat %55, %54, %53, %52, %51, %50, %49, %48 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %17, %73 : i8
                %74 = comb.concat %28, %27, %26, %25, %24, %23, %22, %21 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %20, %74 : i8
            }
        }
        %21 = comb.extract %10 from 0 : (i8) -> i1
        %22 = comb.extract %10 from 1 : (i8) -> i1
        %23 = comb.extract %10 from 2 : (i8) -> i1
        %24 = comb.extract %10 from 3 : (i8) -> i1
        %25 = comb.extract %10 from 4 : (i8) -> i1
        %26 = comb.extract %10 from 5 : (i8) -> i1
        %27 = comb.extract %10 from 6 : (i8) -> i1
        %28 = comb.extract %10 from 7 : (i8) -> i1
        %30 = hw.struct_extract %8["y"] : !hw.struct<x: i8, y: i1>
        %31 = hw.struct_extract %8["x"] : !hw.struct<x: i8, y: i1>
        %32 = comb.extract %31 from 0 : (i8) -> i1
        %33 = comb.extract %31 from 1 : (i8) -> i1
        %34 = comb.extract %31 from 2 : (i8) -> i1
        %35 = comb.extract %31 from 3 : (i8) -> i1
        %36 = comb.extract %31 from 4 : (i8) -> i1
        %37 = comb.extract %31 from 5 : (i8) -> i1
        %38 = comb.extract %31 from 6 : (i8) -> i1
        %39 = comb.extract %31 from 7 : (i8) -> i1
        %40 = comb.extract %2 from 0 : (i8) -> i1
        %41 = comb.extract %2 from 1 : (i8) -> i1
        %42 = comb.extract %2 from 2 : (i8) -> i1
        %43 = comb.extract %2 from 3 : (i8) -> i1
        %44 = comb.extract %2 from 4 : (i8) -> i1
        %45 = comb.extract %2 from 5 : (i8) -> i1
        %46 = comb.extract %2 from 6 : (i8) -> i1
        %47 = comb.extract %2 from 7 : (i8) -> i1
        %48 = comb.extract %4 from 0 : (i8) -> i1
        %49 = comb.extract %4 from 1 : (i8) -> i1
        %50 = comb.extract %4 from 2 : (i8) -> i1
        %51 = comb.extract %4 from 3 : (i8) -> i1
        %52 = comb.extract %4 from 4 : (i8) -> i1
        %53 = comb.extract %4 from 5 : (i8) -> i1
        %54 = comb.extract %4 from 6 : (i8) -> i1
        %55 = comb.extract %4 from 7 : (i8) -> i1
        %60 = hw.struct_extract %7["y"] : !hw.struct<x: i8, y: i1>
        %61 = hw.struct_extract %7["x"] : !hw.struct<x: i8, y: i1>
        %62 = comb.extract %61 from 0 : (i8) -> i1
        %63 = comb.extract %61 from 1 : (i8) -> i1
        %64 = comb.extract %61 from 2 : (i8) -> i1
        %65 = comb.extract %61 from 3 : (i8) -> i1
        %66 = comb.extract %61 from 4 : (i8) -> i1
        %67 = comb.extract %61 from 5 : (i8) -> i1
        %68 = comb.extract %61 from 6 : (i8) -> i1
        %69 = comb.extract %61 from 7 : (i8) -> i1
        %76 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %76, %13 : i1
        %75 = sv.read_inout %76 : !hw.inout<i1>
        %77 = hw.struct_extract %14["x"] : !hw.struct<x: i8, y: i1>
        %78 = comb.extract %77 from 0 : (i8) -> i1
        %80 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %80, %78 : i1
        %79 = sv.read_inout %80 : !hw.inout<i1>
        %81 = comb.extract %77 from 1 : (i8) -> i1
        %83 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i1>
        sv.assign %83, %81 : i1
        %82 = sv.read_inout %83 : !hw.inout<i1>
        %84 = comb.extract %77 from 2 : (i8) -> i1
        %86 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_4 name "_WHEN_ASSERT_4" : !hw.inout<i1>
        sv.assign %86, %84 : i1
        %85 = sv.read_inout %86 : !hw.inout<i1>
        %87 = comb.extract %77 from 3 : (i8) -> i1
        %89 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_5 name "_WHEN_ASSERT_5" : !hw.inout<i1>
        sv.assign %89, %87 : i1
        %88 = sv.read_inout %89 : !hw.inout<i1>
        %90 = comb.extract %77 from 4 : (i8) -> i1
        %92 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_6 name "_WHEN_ASSERT_6" : !hw.inout<i1>
        sv.assign %92, %90 : i1
        %91 = sv.read_inout %92 : !hw.inout<i1>
        %93 = comb.extract %77 from 5 : (i8) -> i1
        %95 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_7 name "_WHEN_ASSERT_7" : !hw.inout<i1>
        sv.assign %95, %93 : i1
        %94 = sv.read_inout %95 : !hw.inout<i1>
        %96 = comb.extract %77 from 6 : (i8) -> i1
        %98 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_8 name "_WHEN_ASSERT_8" : !hw.inout<i1>
        sv.assign %98, %96 : i1
        %97 = sv.read_inout %98 : !hw.inout<i1>
        %99 = comb.extract %77 from 7 : (i8) -> i1
        %101 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_9 name "_WHEN_ASSERT_9" : !hw.inout<i1>
        sv.assign %101, %99 : i1
        %100 = sv.read_inout %101 : !hw.inout<i1>
        %102 = comb.concat %100, %97, %94, %91, %88, %85, %82, %79 : i1, i1, i1, i1, i1, i1, i1, i1
        %103 = hw.struct_extract %14["y"] : !hw.struct<x: i8, y: i1>
        %105 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %105, %103 : i1
        %104 = sv.read_inout %105 : !hw.inout<i1>
        %106 = hw.struct_create (%102, %104) : !hw.struct<x: i8, y: i1>
        %107 = comb.extract %11 from 0 : (i8) -> i1
        %109 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_10 name "_WHEN_ASSERT_10" : !hw.inout<i1>
        sv.assign %109, %107 : i1
        %108 = sv.read_inout %109 : !hw.inout<i1>
        %110 = comb.extract %11 from 1 : (i8) -> i1
        %112 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_11 name "_WHEN_ASSERT_11" : !hw.inout<i1>
        sv.assign %112, %110 : i1
        %111 = sv.read_inout %112 : !hw.inout<i1>
        %113 = comb.extract %11 from 2 : (i8) -> i1
        %115 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_12 name "_WHEN_ASSERT_12" : !hw.inout<i1>
        sv.assign %115, %113 : i1
        %114 = sv.read_inout %115 : !hw.inout<i1>
        %116 = comb.extract %11 from 3 : (i8) -> i1
        %118 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_13 name "_WHEN_ASSERT_13" : !hw.inout<i1>
        sv.assign %118, %116 : i1
        %117 = sv.read_inout %118 : !hw.inout<i1>
        %119 = comb.extract %11 from 4 : (i8) -> i1
        %121 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_14 name "_WHEN_ASSERT_14" : !hw.inout<i1>
        sv.assign %121, %119 : i1
        %120 = sv.read_inout %121 : !hw.inout<i1>
        %122 = comb.extract %11 from 5 : (i8) -> i1
        %124 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_15 name "_WHEN_ASSERT_15" : !hw.inout<i1>
        sv.assign %124, %122 : i1
        %123 = sv.read_inout %124 : !hw.inout<i1>
        %125 = comb.extract %11 from 6 : (i8) -> i1
        %127 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_16 name "_WHEN_ASSERT_16" : !hw.inout<i1>
        sv.assign %127, %125 : i1
        %126 = sv.read_inout %127 : !hw.inout<i1>
        %128 = comb.extract %11 from 7 : (i8) -> i1
        %130 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_17 name "_WHEN_ASSERT_17" : !hw.inout<i1>
        sv.assign %130, %128 : i1
        %129 = sv.read_inout %130 : !hw.inout<i1>
        %131 = comb.concat %129, %126, %123, %120, %117, %114, %111, %108 : i1, i1, i1, i1, i1, i1, i1, i1
        %132 = comb.extract %12 from 0 : (i8) -> i1
        %134 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_18 name "_WHEN_ASSERT_18" : !hw.inout<i1>
        sv.assign %134, %132 : i1
        %133 = sv.read_inout %134 : !hw.inout<i1>
        %135 = comb.extract %12 from 1 : (i8) -> i1
        %137 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_19 name "_WHEN_ASSERT_19" : !hw.inout<i1>
        sv.assign %137, %135 : i1
        %136 = sv.read_inout %137 : !hw.inout<i1>
        %138 = comb.extract %12 from 2 : (i8) -> i1
        %140 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_20 name "_WHEN_ASSERT_20" : !hw.inout<i1>
        sv.assign %140, %138 : i1
        %139 = sv.read_inout %140 : !hw.inout<i1>
        %141 = comb.extract %12 from 3 : (i8) -> i1
        %143 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_21 name "_WHEN_ASSERT_21" : !hw.inout<i1>
        sv.assign %143, %141 : i1
        %142 = sv.read_inout %143 : !hw.inout<i1>
        %144 = comb.extract %12 from 4 : (i8) -> i1
        %146 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_22 name "_WHEN_ASSERT_22" : !hw.inout<i1>
        sv.assign %146, %144 : i1
        %145 = sv.read_inout %146 : !hw.inout<i1>
        %147 = comb.extract %12 from 5 : (i8) -> i1
        %149 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_23 name "_WHEN_ASSERT_23" : !hw.inout<i1>
        sv.assign %149, %147 : i1
        %148 = sv.read_inout %149 : !hw.inout<i1>
        %150 = comb.extract %12 from 6 : (i8) -> i1
        %152 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_24 name "_WHEN_ASSERT_24" : !hw.inout<i1>
        sv.assign %152, %150 : i1
        %151 = sv.read_inout %152 : !hw.inout<i1>
        %153 = comb.extract %12 from 7 : (i8) -> i1
        %155 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_25 name "_WHEN_ASSERT_25" : !hw.inout<i1>
        sv.assign %155, %153 : i1
        %154 = sv.read_inout %155 : !hw.inout<i1>
        %156 = comb.concat %154, %151, %148, %145, %142, %139, %136, %133 : i1, i1, i1, i1, i1, i1, i1, i1
        %157 = hw.array_create %156, %131 : i8
        %158 = hw.struct_create (%75, %106, %157) : !hw.struct<y: i1, z: !hw.struct<x: i8, y: i1>, x: !hw.array<2xi8>>
        %159 = comb.extract %15 from 0 : (i8) -> i1
        %161 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_26 name "_WHEN_ASSERT_26" : !hw.inout<i1>
        sv.assign %161, %159 : i1
        %160 = sv.read_inout %161 : !hw.inout<i1>
        %162 = comb.extract %15 from 1 : (i8) -> i1
        %164 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_27 name "_WHEN_ASSERT_27" : !hw.inout<i1>
        sv.assign %164, %162 : i1
        %163 = sv.read_inout %164 : !hw.inout<i1>
        %165 = comb.extract %15 from 2 : (i8) -> i1
        %167 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_28 name "_WHEN_ASSERT_28" : !hw.inout<i1>
        sv.assign %167, %165 : i1
        %166 = sv.read_inout %167 : !hw.inout<i1>
        %168 = comb.extract %15 from 3 : (i8) -> i1
        %170 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_29 name "_WHEN_ASSERT_29" : !hw.inout<i1>
        sv.assign %170, %168 : i1
        %169 = sv.read_inout %170 : !hw.inout<i1>
        %171 = comb.extract %15 from 4 : (i8) -> i1
        %173 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_30 name "_WHEN_ASSERT_30" : !hw.inout<i1>
        sv.assign %173, %171 : i1
        %172 = sv.read_inout %173 : !hw.inout<i1>
        %174 = comb.extract %15 from 5 : (i8) -> i1
        %176 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_31 name "_WHEN_ASSERT_31" : !hw.inout<i1>
        sv.assign %176, %174 : i1
        %175 = sv.read_inout %176 : !hw.inout<i1>
        %177 = comb.extract %15 from 6 : (i8) -> i1
        %179 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_32 name "_WHEN_ASSERT_32" : !hw.inout<i1>
        sv.assign %179, %177 : i1
        %178 = sv.read_inout %179 : !hw.inout<i1>
        %180 = comb.extract %15 from 7 : (i8) -> i1
        %182 = sv.wire sym @test_when_tuple_as_bits_resolve_False._WHEN_ASSERT_33 name "_WHEN_ASSERT_33" : !hw.inout<i1>
        sv.assign %182, %180 : i1
        %181 = sv.read_inout %182 : !hw.inout<i1>
        %183 = comb.concat %181, %178, %175, %172, %169, %166, %163, %160 : i1, i1, i1, i1, i1, i1, i1, i1
        %184 = hw.struct_create (%158, %183) : !hw.struct<x: !hw.struct<y: i1, z: !hw.struct<x: i8, y: i1>, x: !hw.array<2xi8>>, y: i8>
        %185 = comb.concat %181, %178, %175, %172, %169, %166, %163, %160, %154, %151, %148, %145, %142, %139, %136, %133, %129, %126, %123, %120, %117, %114, %111, %108, %104, %100, %97, %94, %91, %88, %85, %82, %79, %75 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %75, %6) : i1, i1, i1
        %186 = hw.struct_extract %8["y"] : !hw.struct<x: i8, y: i1>
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %104, %186) : i1, i1, i1
        %187 = hw.struct_extract %8["x"] : !hw.struct<x: i8, y: i1>
        %188 = comb.extract %187 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %79, %188) : i1, i1, i1
        %189 = comb.extract %187 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %82, %189) : i1, i1, i1
        %190 = comb.extract %187 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %85, %190) : i1, i1, i1
        %191 = comb.extract %187 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %88, %191) : i1, i1, i1
        %192 = comb.extract %187 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %91, %192) : i1, i1, i1
        %193 = comb.extract %187 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %94, %193) : i1, i1, i1
        %194 = comb.extract %187 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %97, %194) : i1, i1, i1
        %195 = comb.extract %187 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_9: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %100, %195) : i1, i1, i1
        %196 = comb.extract %2 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_10: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %108, %196) : i1, i1, i1
        %197 = comb.extract %2 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_11: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %111, %197) : i1, i1, i1
        %198 = comb.extract %2 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_12: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %114, %198) : i1, i1, i1
        %199 = comb.extract %2 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_13: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %117, %199) : i1, i1, i1
        %200 = comb.extract %2 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_14: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %120, %200) : i1, i1, i1
        %201 = comb.extract %2 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_15: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %123, %201) : i1, i1, i1
        %202 = comb.extract %2 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_16: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %126, %202) : i1, i1, i1
        %203 = comb.extract %2 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_17: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %129, %203) : i1, i1, i1
        %204 = comb.extract %4 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_18: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %133, %204) : i1, i1, i1
        %205 = comb.extract %4 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_19: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %136, %205) : i1, i1, i1
        %206 = comb.extract %4 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_20: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %139, %206) : i1, i1, i1
        %207 = comb.extract %4 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_21: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %142, %207) : i1, i1, i1
        %208 = comb.extract %4 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_22: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %145, %208) : i1, i1, i1
        %209 = comb.extract %4 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_23: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %148, %209) : i1, i1, i1
        %210 = comb.extract %4 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_24: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %151, %210) : i1, i1, i1
        %211 = comb.extract %4 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_25: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %154, %211) : i1, i1, i1
        %213 = hw.constant -1 : i1
        %212 = comb.xor %213, %S : i1
        sv.verbatim "WHEN_ASSERT_26: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %75, %6) : i1, i1, i1
        %214 = hw.struct_extract %7["y"] : !hw.struct<x: i8, y: i1>
        sv.verbatim "WHEN_ASSERT_27: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %104, %214) : i1, i1, i1
        %215 = hw.struct_extract %7["x"] : !hw.struct<x: i8, y: i1>
        %216 = comb.extract %215 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_28: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %79, %216) : i1, i1, i1
        %217 = comb.extract %215 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_29: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %82, %217) : i1, i1, i1
        %218 = comb.extract %215 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_30: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %85, %218) : i1, i1, i1
        %219 = comb.extract %215 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_31: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %88, %219) : i1, i1, i1
        %220 = comb.extract %215 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_32: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %91, %220) : i1, i1, i1
        %221 = comb.extract %215 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_33: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %94, %221) : i1, i1, i1
        %222 = comb.extract %215 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_34: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %97, %222) : i1, i1, i1
        %223 = comb.extract %215 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_35: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %100, %223) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_36: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %108, %196) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_37: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %111, %197) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_38: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %114, %198) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_39: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %117, %199) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_40: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %120, %200) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_41: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %123, %201) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_42: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %126, %202) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_43: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %129, %203) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_44: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %133, %204) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_45: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %136, %205) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_46: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %139, %206) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_47: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %142, %207) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_48: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %145, %208) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_49: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %148, %209) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_50: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %151, %210) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_51: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %154, %211) : i1, i1, i1
        %224 = comb.extract %10 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_52: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %160, %224) : i1, i1, i1
        %225 = comb.extract %10 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_53: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %163, %225) : i1, i1, i1
        %226 = comb.extract %10 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_54: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %166, %226) : i1, i1, i1
        %227 = comb.extract %10 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_55: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %169, %227) : i1, i1, i1
        %228 = comb.extract %10 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_56: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %172, %228) : i1, i1, i1
        %229 = comb.extract %10 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_57: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %175, %229) : i1, i1, i1
        %230 = comb.extract %10 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_58: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %178, %230) : i1, i1, i1
        %231 = comb.extract %10 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_59: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%212, %181, %231) : i1, i1, i1
        %232 = comb.xor %213, %212 : i1
        sv.verbatim "WHEN_ASSERT_60: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%232, %160, %224) : i1, i1, i1
        %233 = comb.xor %213, %212 : i1
        sv.verbatim "WHEN_ASSERT_61: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%233, %163, %225) : i1, i1, i1
        %234 = comb.xor %213, %212 : i1
        sv.verbatim "WHEN_ASSERT_62: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%234, %166, %226) : i1, i1, i1
        %235 = comb.xor %213, %212 : i1
        sv.verbatim "WHEN_ASSERT_63: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%235, %169, %227) : i1, i1, i1
        %236 = comb.xor %213, %212 : i1
        sv.verbatim "WHEN_ASSERT_64: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%236, %172, %228) : i1, i1, i1
        %237 = comb.xor %213, %212 : i1
        sv.verbatim "WHEN_ASSERT_65: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%237, %175, %229) : i1, i1, i1
        %238 = comb.xor %213, %212 : i1
        sv.verbatim "WHEN_ASSERT_66: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%238, %178, %230) : i1, i1, i1
        %239 = comb.xor %213, %212 : i1
        sv.verbatim "WHEN_ASSERT_67: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%239, %181, %231) : i1, i1, i1
        hw.output %184, %185 : !hw.struct<x: !hw.struct<y: i1, z: !hw.struct<x: i8, y: i1>, x: !hw.array<2xi8>>, y: i8>, i34
    }
}
