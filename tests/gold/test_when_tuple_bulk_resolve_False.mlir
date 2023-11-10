module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_tuple_bulk_resolve_False(in %I: !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>, in %S: i2, in %CLK: i1, out O: !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %2 = hw.struct_extract %1["x"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %4 = sv.wire sym @test_when_tuple_bulk_resolve_False._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i8>
        sv.assign %4, %2 : i8
        %3 = sv.read_inout %4 : !hw.inout<i8>
        %5 = hw.struct_extract %1["y"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %6 = hw.struct_extract %5["x"] : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %7 = hw.struct_extract %6["x"] : !hw.struct<x: i8, y: i8>
        %9 = sv.wire sym @test_when_tuple_bulk_resolve_False._WHEN_ASSERT_4 name "_WHEN_ASSERT_4" : !hw.inout<i8>
        sv.assign %9, %7 : i8
        %8 = sv.read_inout %9 : !hw.inout<i8>
        %10 = hw.struct_extract %6["y"] : !hw.struct<x: i8, y: i8>
        %12 = sv.wire sym @test_when_tuple_bulk_resolve_False._WHEN_ASSERT_5 name "_WHEN_ASSERT_5" : !hw.inout<i8>
        sv.assign %12, %10 : i8
        %11 = sv.read_inout %12 : !hw.inout<i8>
        %13 = hw.struct_create (%8, %11) : !hw.struct<x: i8, y: i8>
        %14 = hw.struct_extract %5["y"] : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %15 = hw.struct_extract %14["x"] : !hw.struct<x: i8, y: i8>
        %17 = sv.wire sym @test_when_tuple_bulk_resolve_False._WHEN_ASSERT_6 name "_WHEN_ASSERT_6" : !hw.inout<i8>
        sv.assign %17, %15 : i8
        %16 = sv.read_inout %17 : !hw.inout<i8>
        %18 = hw.struct_extract %14["y"] : !hw.struct<x: i8, y: i8>
        %20 = sv.wire sym @test_when_tuple_bulk_resolve_False._WHEN_ASSERT_7 name "_WHEN_ASSERT_7" : !hw.inout<i8>
        sv.assign %20, %18 : i8
        %19 = sv.read_inout %20 : !hw.inout<i8>
        %21 = hw.struct_create (%16, %19) : !hw.struct<x: i8, y: i8>
        %22 = hw.struct_create (%13, %21) : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %23 = hw.struct_create (%3, %22) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %25 = sv.reg name "y" : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        sv.alwaysff(posedge %CLK) {
            sv.passign %25, %23 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        }
        %27 = hw.constant 0 : i8
        %30 = hw.constant 0 : i8
        %31 = hw.constant 0 : i8
        %29 = hw.struct_create (%30, %31) : !hw.struct<x: i8, y: i8>
        %33 = hw.constant 0 : i8
        %34 = hw.constant 0 : i8
        %32 = hw.struct_create (%33, %34) : !hw.struct<x: i8, y: i8>
        %28 = hw.struct_create (%29, %32) : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %26 = hw.struct_create (%27, %28) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        sv.initial {
            sv.bpassign %25, %26 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        }
        %24 = sv.read_inout %25 : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        %35 = comb.extract %S from 1 : (i2) -> i1
        %36 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %37 = hw.struct_extract %I["y"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %40 = sv.reg : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        %39 = sv.read_inout %40 : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        %41 = sv.reg : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        %1 = sv.read_inout %41 : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        sv.alwayscomb {
            sv.if %0 {
                %60 = hw.struct_create (%53, %54) : !hw.struct<x: i8, y: i8>
                %61 = hw.struct_create (%56, %57) : !hw.struct<x: i8, y: i8>
                %59 = hw.struct_create (%60, %61) : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
                %58 = hw.struct_create (%42, %59) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                sv.bpassign %40, %58 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                %64 = hw.struct_create (%46, %47) : !hw.struct<x: i8, y: i8>
                %65 = hw.struct_create (%49, %50) : !hw.struct<x: i8, y: i8>
                %63 = hw.struct_create (%64, %65) : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
                %62 = hw.struct_create (%43, %63) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                sv.bpassign %41, %62 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
            } else {
                %68 = hw.struct_create (%53, %54) : !hw.struct<x: i8, y: i8>
                %69 = hw.struct_create (%56, %57) : !hw.struct<x: i8, y: i8>
                %67 = hw.struct_create (%68, %69) : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
                %66 = hw.struct_create (%42, %67) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                sv.bpassign %41, %66 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                sv.if %35 {
                    %78 = hw.struct_create (%71, %72) : !hw.struct<x: i8, y: i8>
                    %79 = hw.struct_create (%74, %75) : !hw.struct<x: i8, y: i8>
                    %77 = hw.struct_create (%78, %79) : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
                    %76 = hw.struct_create (%36, %77) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                    sv.bpassign %40, %76 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                } else {
                    %82 = hw.struct_create (%53, %54) : !hw.struct<x: i8, y: i8>
                    %83 = hw.struct_create (%56, %57) : !hw.struct<x: i8, y: i8>
                    %81 = hw.struct_create (%82, %83) : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
                    %80 = hw.struct_create (%42, %81) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                    sv.bpassign %40, %80 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                }
            }
        }
        %42 = hw.struct_extract %38["x"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %43 = hw.struct_extract %24["x"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %44 = hw.struct_extract %24["y"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %45 = hw.struct_extract %44["x"] : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %46 = hw.struct_extract %45["x"] : !hw.struct<x: i8, y: i8>
        %47 = hw.struct_extract %45["y"] : !hw.struct<x: i8, y: i8>
        %48 = hw.struct_extract %44["y"] : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %49 = hw.struct_extract %48["x"] : !hw.struct<x: i8, y: i8>
        %50 = hw.struct_extract %48["y"] : !hw.struct<x: i8, y: i8>
        %51 = hw.struct_extract %38["y"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %52 = hw.struct_extract %51["x"] : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %53 = hw.struct_extract %52["x"] : !hw.struct<x: i8, y: i8>
        %54 = hw.struct_extract %52["y"] : !hw.struct<x: i8, y: i8>
        %55 = hw.struct_extract %51["y"] : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %56 = hw.struct_extract %55["x"] : !hw.struct<x: i8, y: i8>
        %57 = hw.struct_extract %55["y"] : !hw.struct<x: i8, y: i8>
        %70 = hw.struct_extract %37["x"] : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %71 = hw.struct_extract %70["x"] : !hw.struct<x: i8, y: i8>
        %72 = hw.struct_extract %70["y"] : !hw.struct<x: i8, y: i8>
        %73 = hw.struct_extract %37["y"] : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %74 = hw.struct_extract %73["x"] : !hw.struct<x: i8, y: i8>
        %75 = hw.struct_extract %73["y"] : !hw.struct<x: i8, y: i8>
        %84 = hw.struct_extract %39["x"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %86 = sv.wire sym @test_when_tuple_bulk_resolve_False._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i8>
        sv.assign %86, %84 : i8
        %85 = sv.read_inout %86 : !hw.inout<i8>
        %87 = hw.struct_extract %39["y"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %88 = hw.struct_extract %87["x"] : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %89 = hw.struct_extract %88["x"] : !hw.struct<x: i8, y: i8>
        %91 = sv.wire sym @test_when_tuple_bulk_resolve_False._WHEN_ASSERT_10 name "_WHEN_ASSERT_10" : !hw.inout<i8>
        sv.assign %91, %89 : i8
        %90 = sv.read_inout %91 : !hw.inout<i8>
        %92 = hw.struct_extract %88["y"] : !hw.struct<x: i8, y: i8>
        %94 = sv.wire sym @test_when_tuple_bulk_resolve_False._WHEN_ASSERT_11 name "_WHEN_ASSERT_11" : !hw.inout<i8>
        sv.assign %94, %92 : i8
        %93 = sv.read_inout %94 : !hw.inout<i8>
        %95 = hw.struct_create (%90, %93) : !hw.struct<x: i8, y: i8>
        %96 = hw.struct_extract %87["y"] : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %97 = hw.struct_extract %96["x"] : !hw.struct<x: i8, y: i8>
        %99 = sv.wire sym @test_when_tuple_bulk_resolve_False._WHEN_ASSERT_12 name "_WHEN_ASSERT_12" : !hw.inout<i8>
        sv.assign %99, %97 : i8
        %98 = sv.read_inout %99 : !hw.inout<i8>
        %100 = hw.struct_extract %96["y"] : !hw.struct<x: i8, y: i8>
        %102 = sv.wire sym @test_when_tuple_bulk_resolve_False._WHEN_ASSERT_13 name "_WHEN_ASSERT_13" : !hw.inout<i8>
        sv.assign %102, %100 : i8
        %101 = sv.read_inout %102 : !hw.inout<i8>
        %103 = hw.struct_create (%98, %101) : !hw.struct<x: i8, y: i8>
        %104 = hw.struct_create (%95, %103) : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %105 = hw.struct_create (%85, %104) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %106 = sv.reg name "x" : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        sv.alwaysff(posedge %CLK) {
            sv.passign %106, %105 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        }
        sv.initial {
            sv.bpassign %106, %26 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        }
        %38 = sv.read_inout %106 : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        %107 = hw.struct_extract %38["x"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %85, %107) : i1, i8, i8
        %108 = hw.struct_create (%90, %93) : !hw.struct<x: i8, y: i8>
        %110 = sv.wire sym @test_when_tuple_bulk_resolve_False._WHEN_ASSERT_8 name "_WHEN_ASSERT_8" : !hw.inout<!hw.struct<x: i8, y: i8>>
        sv.assign %110, %108 : !hw.struct<x: i8, y: i8>
        %109 = sv.read_inout %110 : !hw.inout<!hw.struct<x: i8, y: i8>>
        %111 = hw.struct_create (%98, %101) : !hw.struct<x: i8, y: i8>
        %113 = sv.wire sym @test_when_tuple_bulk_resolve_False._WHEN_ASSERT_9 name "_WHEN_ASSERT_9" : !hw.inout<!hw.struct<x: i8, y: i8>>
        sv.assign %113, %111 : !hw.struct<x: i8, y: i8>
        %112 = sv.read_inout %113 : !hw.inout<!hw.struct<x: i8, y: i8>>
        %114 = hw.struct_create (%109, %112) : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %116 = sv.wire sym @test_when_tuple_bulk_resolve_False._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<!hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        sv.assign %116, %114 : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %115 = sv.read_inout %116 : !hw.inout<!hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %117 = hw.struct_extract %115["y"] : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %118 = hw.struct_extract %117["y"] : !hw.struct<x: i8, y: i8>
        %119 = hw.struct_extract %117["x"] : !hw.struct<x: i8, y: i8>
        %120 = hw.struct_extract %115["x"] : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %121 = hw.struct_extract %120["y"] : !hw.struct<x: i8, y: i8>
        %122 = hw.struct_extract %120["x"] : !hw.struct<x: i8, y: i8>
        %123 = hw.struct_extract %38["y"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %124 = hw.struct_extract %123["y"] : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %125 = hw.struct_extract %124["y"] : !hw.struct<x: i8, y: i8>
        %126 = hw.struct_extract %124["x"] : !hw.struct<x: i8, y: i8>
        %127 = hw.struct_extract %123["x"] : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %128 = hw.struct_extract %127["y"] : !hw.struct<x: i8, y: i8>
        %129 = hw.struct_extract %127["x"] : !hw.struct<x: i8, y: i8>
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{{{1}}, {{2}}}, {{{3}}, {{4}}}} == {{{{5}}, {{6}}}, {{{7}}, {{8}}}}));" (%0, %118, %119, %121, %122, %125, %126, %128, %129) : i1, i8, i8, i8, i8, i8, i8, i8, i8
        %130 = hw.struct_extract %24["x"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %3, %130) : i1, i8, i8
        %131 = hw.struct_create (%8, %11) : !hw.struct<x: i8, y: i8>
        %132 = hw.struct_create (%16, %19) : !hw.struct<x: i8, y: i8>
        %133 = hw.struct_create (%131, %132) : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %135 = sv.wire sym @test_when_tuple_bulk_resolve_False._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<!hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        sv.assign %135, %133 : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %134 = sv.read_inout %135 : !hw.inout<!hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %136 = hw.struct_extract %134["y"] : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %137 = hw.struct_extract %136["y"] : !hw.struct<x: i8, y: i8>
        %138 = hw.struct_extract %136["x"] : !hw.struct<x: i8, y: i8>
        %139 = hw.struct_extract %134["x"] : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %140 = hw.struct_extract %139["y"] : !hw.struct<x: i8, y: i8>
        %141 = hw.struct_extract %139["x"] : !hw.struct<x: i8, y: i8>
        %142 = hw.struct_extract %24["y"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %143 = hw.struct_extract %142["y"] : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %144 = hw.struct_extract %143["y"] : !hw.struct<x: i8, y: i8>
        %145 = hw.struct_extract %143["x"] : !hw.struct<x: i8, y: i8>
        %146 = hw.struct_extract %142["x"] : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %147 = hw.struct_extract %146["y"] : !hw.struct<x: i8, y: i8>
        %148 = hw.struct_extract %146["x"] : !hw.struct<x: i8, y: i8>
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{{{1}}, {{2}}}, {{{3}}, {{4}}}} == {{{{5}}, {{6}}}, {{{7}}, {{8}}}}));" (%0, %137, %138, %140, %141, %144, %145, %147, %148) : i1, i8, i8, i8, i8, i8, i8, i8, i8
        %150 = hw.constant -1 : i1
        %149 = comb.xor %150, %0 : i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%149, %3, %107) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%149, %8, %129) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%149, %11, %128) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%149, %16, %126) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%149, %19, %125) : i1, i8, i8
        %151 = comb.and %149, %35 : i1
        sv.verbatim "WHEN_ASSERT_9: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%151, %85, %36) : i1, i8, i8
        %152 = hw.struct_extract %109["y"] : !hw.struct<x: i8, y: i8>
        %153 = hw.struct_extract %109["x"] : !hw.struct<x: i8, y: i8>
        %154 = hw.struct_extract %37["x"] : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %155 = hw.struct_extract %154["y"] : !hw.struct<x: i8, y: i8>
        %156 = hw.struct_extract %154["x"] : !hw.struct<x: i8, y: i8>
        sv.verbatim "WHEN_ASSERT_10: assert property (({{0}}) |-> ({{{1}}, {{2}}} == {{{3}}, {{4}}}));" (%151, %152, %153, %155, %156) : i1, i8, i8, i8, i8
        %157 = hw.struct_extract %112["y"] : !hw.struct<x: i8, y: i8>
        %158 = hw.struct_extract %112["x"] : !hw.struct<x: i8, y: i8>
        %159 = hw.struct_extract %37["y"] : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %160 = hw.struct_extract %159["y"] : !hw.struct<x: i8, y: i8>
        %161 = hw.struct_extract %159["x"] : !hw.struct<x: i8, y: i8>
        sv.verbatim "WHEN_ASSERT_11: assert property (({{0}}) |-> ({{{1}}, {{2}}} == {{{3}}, {{4}}}));" (%151, %157, %158, %160, %161) : i1, i8, i8, i8, i8
        %162 = comb.xor %150, %35 : i1
        %163 = comb.and %149, %162 : i1
        sv.verbatim "WHEN_ASSERT_12: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%163, %85, %107) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_13: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%163, %90, %129) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_14: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%163, %93, %128) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_15: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%163, %98, %126) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_16: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%163, %101, %125) : i1, i8, i8
        hw.output %38 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
    }
}
