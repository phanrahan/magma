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
        %50 = sv.reg : !hw.inout<i8>
        %11 = sv.read_inout %50 : !hw.inout<i8>
        %51 = sv.reg : !hw.inout<i8>
        %12 = sv.read_inout %51 : !hw.inout<i8>
        %52 = sv.reg : !hw.inout<i1>
        %13 = sv.read_inout %52 : !hw.inout<i1>
        %53 = sv.reg : !hw.inout<!hw.struct<x: i8, y: i1>>
        %14 = sv.read_inout %53 : !hw.inout<!hw.struct<x: i8, y: i1>>
        %54 = sv.reg : !hw.inout<i8>
        %15 = sv.read_inout %54 : !hw.inout<i8>
        %55 = sv.reg : !hw.inout<i1>
        %16 = sv.read_inout %55 : !hw.inout<i1>
        %56 = sv.reg : !hw.inout<i1>
        %17 = sv.read_inout %56 : !hw.inout<i1>
        %57 = sv.reg : !hw.inout<i1>
        %18 = sv.read_inout %57 : !hw.inout<i1>
        %58 = sv.reg : !hw.inout<i1>
        %19 = sv.read_inout %58 : !hw.inout<i1>
        %59 = sv.reg : !hw.inout<i1>
        %20 = sv.read_inout %59 : !hw.inout<i1>
        %60 = sv.reg : !hw.inout<i1>
        %21 = sv.read_inout %60 : !hw.inout<i1>
        %61 = sv.reg : !hw.inout<i1>
        %22 = sv.read_inout %61 : !hw.inout<i1>
        %62 = sv.reg : !hw.inout<i1>
        %23 = sv.read_inout %62 : !hw.inout<i1>
        %63 = sv.reg : !hw.inout<i1>
        %24 = sv.read_inout %63 : !hw.inout<i1>
        %64 = sv.reg : !hw.inout<i1>
        %25 = sv.read_inout %64 : !hw.inout<i1>
        %65 = sv.reg : !hw.inout<i1>
        %26 = sv.read_inout %65 : !hw.inout<i1>
        %66 = sv.reg : !hw.inout<i1>
        %27 = sv.read_inout %66 : !hw.inout<i1>
        %67 = sv.reg : !hw.inout<i1>
        %28 = sv.read_inout %67 : !hw.inout<i1>
        %68 = sv.reg : !hw.inout<i1>
        %29 = sv.read_inout %68 : !hw.inout<i1>
        %69 = sv.reg : !hw.inout<i1>
        %30 = sv.read_inout %69 : !hw.inout<i1>
        %70 = sv.reg : !hw.inout<i1>
        %31 = sv.read_inout %70 : !hw.inout<i1>
        %71 = sv.reg : !hw.inout<i1>
        %32 = sv.read_inout %71 : !hw.inout<i1>
        %72 = sv.reg : !hw.inout<i1>
        %33 = sv.read_inout %72 : !hw.inout<i1>
        %73 = sv.reg : !hw.inout<i1>
        %34 = sv.read_inout %73 : !hw.inout<i1>
        %74 = sv.reg : !hw.inout<i1>
        %35 = sv.read_inout %74 : !hw.inout<i1>
        %75 = sv.reg : !hw.inout<i1>
        %36 = sv.read_inout %75 : !hw.inout<i1>
        %76 = sv.reg : !hw.inout<i1>
        %37 = sv.read_inout %76 : !hw.inout<i1>
        %77 = sv.reg : !hw.inout<i1>
        %38 = sv.read_inout %77 : !hw.inout<i1>
        %78 = sv.reg : !hw.inout<i1>
        %39 = sv.read_inout %78 : !hw.inout<i1>
        %79 = sv.reg : !hw.inout<i1>
        %40 = sv.read_inout %79 : !hw.inout<i1>
        %80 = sv.reg : !hw.inout<i1>
        %41 = sv.read_inout %80 : !hw.inout<i1>
        %81 = sv.reg : !hw.inout<i1>
        %42 = sv.read_inout %81 : !hw.inout<i1>
        %82 = sv.reg : !hw.inout<i1>
        %43 = sv.read_inout %82 : !hw.inout<i1>
        %83 = sv.reg : !hw.inout<i1>
        %44 = sv.read_inout %83 : !hw.inout<i1>
        %84 = sv.reg : !hw.inout<i1>
        %45 = sv.read_inout %84 : !hw.inout<i1>
        %85 = sv.reg : !hw.inout<i1>
        %46 = sv.read_inout %85 : !hw.inout<i1>
        %86 = sv.reg : !hw.inout<i1>
        %47 = sv.read_inout %86 : !hw.inout<i1>
        %87 = sv.reg : !hw.inout<i1>
        %48 = sv.read_inout %87 : !hw.inout<i1>
        %88 = sv.reg : !hw.inout<i1>
        %49 = sv.read_inout %88 : !hw.inout<i1>
        sv.alwayscomb {
            %97 = comb.concat %96, %95, %94, %93, %92, %91, %90, %89 : i1, i1, i1, i1, i1, i1, i1, i1
            sv.bpassign %54, %97 : i8
            sv.bpassign %81, %89 : i1
            sv.bpassign %82, %90 : i1
            sv.bpassign %83, %91 : i1
            sv.bpassign %84, %92 : i1
            sv.bpassign %85, %93 : i1
            sv.bpassign %86, %94 : i1
            sv.bpassign %87, %95 : i1
            sv.bpassign %88, %96 : i1
            sv.if %S {
                sv.bpassign %52, %6 : i1
                sv.bpassign %55, %6 : i1
                %125 = comb.concat %107, %106, %105, %104, %103, %102, %101, %100 : i1, i1, i1, i1, i1, i1, i1, i1
                %124 = hw.struct_create (%125, %98) : !hw.struct<x: i8, y: i1>
                sv.bpassign %53, %124 : !hw.struct<x: i8, y: i1>
                sv.bpassign %56, %100 : i1
                sv.bpassign %57, %101 : i1
                sv.bpassign %58, %102 : i1
                sv.bpassign %59, %103 : i1
                sv.bpassign %60, %104 : i1
                sv.bpassign %61, %105 : i1
                sv.bpassign %62, %106 : i1
                sv.bpassign %63, %107 : i1
                sv.bpassign %64, %98 : i1
                %126 = comb.concat %115, %114, %113, %112, %111, %110, %109, %108 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %50, %126 : i8
                sv.bpassign %65, %108 : i1
                sv.bpassign %66, %109 : i1
                sv.bpassign %67, %110 : i1
                sv.bpassign %68, %111 : i1
                sv.bpassign %69, %112 : i1
                sv.bpassign %70, %113 : i1
                sv.bpassign %71, %114 : i1
                sv.bpassign %72, %115 : i1
                %127 = comb.concat %123, %122, %121, %120, %119, %118, %117, %116 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %51, %127 : i8
                sv.bpassign %73, %116 : i1
                sv.bpassign %74, %117 : i1
                sv.bpassign %75, %118 : i1
                sv.bpassign %76, %119 : i1
                sv.bpassign %77, %120 : i1
                sv.bpassign %78, %121 : i1
                sv.bpassign %79, %122 : i1
                sv.bpassign %80, %123 : i1
            } else {
                sv.bpassign %52, %6 : i1
                sv.bpassign %55, %6 : i1
                %139 = comb.concat %137, %136, %135, %134, %133, %132, %131, %130 : i1, i1, i1, i1, i1, i1, i1, i1
                %138 = hw.struct_create (%139, %128) : !hw.struct<x: i8, y: i1>
                sv.bpassign %53, %138 : !hw.struct<x: i8, y: i1>
                sv.bpassign %56, %130 : i1
                sv.bpassign %57, %131 : i1
                sv.bpassign %58, %132 : i1
                sv.bpassign %59, %133 : i1
                sv.bpassign %60, %134 : i1
                sv.bpassign %61, %135 : i1
                sv.bpassign %62, %136 : i1
                sv.bpassign %63, %137 : i1
                sv.bpassign %64, %128 : i1
                %140 = comb.concat %115, %114, %113, %112, %111, %110, %109, %108 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %50, %140 : i8
                sv.bpassign %65, %108 : i1
                sv.bpassign %66, %109 : i1
                sv.bpassign %67, %110 : i1
                sv.bpassign %68, %111 : i1
                sv.bpassign %69, %112 : i1
                sv.bpassign %70, %113 : i1
                sv.bpassign %71, %114 : i1
                sv.bpassign %72, %115 : i1
                %141 = comb.concat %123, %122, %121, %120, %119, %118, %117, %116 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %51, %141 : i8
                sv.bpassign %73, %116 : i1
                sv.bpassign %74, %117 : i1
                sv.bpassign %75, %118 : i1
                sv.bpassign %76, %119 : i1
                sv.bpassign %77, %120 : i1
                sv.bpassign %78, %121 : i1
                sv.bpassign %79, %122 : i1
                sv.bpassign %80, %123 : i1
                %142 = comb.concat %96, %95, %94, %93, %92, %91, %90, %89 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %54, %142 : i8
                sv.bpassign %81, %89 : i1
                sv.bpassign %82, %90 : i1
                sv.bpassign %83, %91 : i1
                sv.bpassign %84, %92 : i1
                sv.bpassign %85, %93 : i1
                sv.bpassign %86, %94 : i1
                sv.bpassign %87, %95 : i1
                sv.bpassign %88, %96 : i1
            }
        }
        %89 = comb.extract %10 from 0 : (i8) -> i1
        %90 = comb.extract %10 from 1 : (i8) -> i1
        %91 = comb.extract %10 from 2 : (i8) -> i1
        %92 = comb.extract %10 from 3 : (i8) -> i1
        %93 = comb.extract %10 from 4 : (i8) -> i1
        %94 = comb.extract %10 from 5 : (i8) -> i1
        %95 = comb.extract %10 from 6 : (i8) -> i1
        %96 = comb.extract %10 from 7 : (i8) -> i1
        %98 = hw.struct_extract %8["y"] : !hw.struct<x: i8, y: i1>
        %99 = hw.struct_extract %8["x"] : !hw.struct<x: i8, y: i1>
        %100 = comb.extract %99 from 0 : (i8) -> i1
        %101 = comb.extract %99 from 1 : (i8) -> i1
        %102 = comb.extract %99 from 2 : (i8) -> i1
        %103 = comb.extract %99 from 3 : (i8) -> i1
        %104 = comb.extract %99 from 4 : (i8) -> i1
        %105 = comb.extract %99 from 5 : (i8) -> i1
        %106 = comb.extract %99 from 6 : (i8) -> i1
        %107 = comb.extract %99 from 7 : (i8) -> i1
        %108 = comb.extract %2 from 0 : (i8) -> i1
        %109 = comb.extract %2 from 1 : (i8) -> i1
        %110 = comb.extract %2 from 2 : (i8) -> i1
        %111 = comb.extract %2 from 3 : (i8) -> i1
        %112 = comb.extract %2 from 4 : (i8) -> i1
        %113 = comb.extract %2 from 5 : (i8) -> i1
        %114 = comb.extract %2 from 6 : (i8) -> i1
        %115 = comb.extract %2 from 7 : (i8) -> i1
        %116 = comb.extract %4 from 0 : (i8) -> i1
        %117 = comb.extract %4 from 1 : (i8) -> i1
        %118 = comb.extract %4 from 2 : (i8) -> i1
        %119 = comb.extract %4 from 3 : (i8) -> i1
        %120 = comb.extract %4 from 4 : (i8) -> i1
        %121 = comb.extract %4 from 5 : (i8) -> i1
        %122 = comb.extract %4 from 6 : (i8) -> i1
        %123 = comb.extract %4 from 7 : (i8) -> i1
        %128 = hw.struct_extract %7["y"] : !hw.struct<x: i8, y: i1>
        %129 = hw.struct_extract %7["x"] : !hw.struct<x: i8, y: i1>
        %130 = comb.extract %129 from 0 : (i8) -> i1
        %131 = comb.extract %129 from 1 : (i8) -> i1
        %132 = comb.extract %129 from 2 : (i8) -> i1
        %133 = comb.extract %129 from 3 : (i8) -> i1
        %134 = comb.extract %129 from 4 : (i8) -> i1
        %135 = comb.extract %129 from 5 : (i8) -> i1
        %136 = comb.extract %129 from 6 : (i8) -> i1
        %137 = comb.extract %129 from 7 : (i8) -> i1
        %143 = hw.array_create %12, %11 : i8
        %144 = hw.struct_create (%13, %14, %143) : !hw.struct<y: i1, z: !hw.struct<x: i8, y: i1>, x: !hw.array<2xi8>>
        %145 = hw.struct_create (%144, %15) : !hw.struct<x: !hw.struct<y: i1, z: !hw.struct<x: i8, y: i1>, x: !hw.array<2xi8>>, y: i8>
        %146 = comb.concat %49, %48, %47, %46, %45, %44, %43, %42, %41, %40, %39, %38, %37, %36, %35, %34, %33, %32, %31, %30, %29, %28, %27, %26, %25, %24, %23, %22, %21, %20, %19, %18, %17, %16 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        hw.output %145, %146 : !hw.struct<x: !hw.struct<y: i1, z: !hw.struct<x: i8, y: i1>, x: !hw.array<2xi8>>, y: i8>, i34
    }
}
