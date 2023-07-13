module attributes {circt.loweringOptions = "locationInfoStyle=none,disallowLocalVariables"} {
    hw.module @test_when_tuple_as_bits_resolve_False(%I: !hw.struct<x: !hw.struct<x: !hw.array<2xi8>, y: i1, z: !hw.struct<x: i8, y: i1>>, y: i8>, %S: i1) -> (O: !hw.struct<x: !hw.struct<x: !hw.array<2xi8>, y: i1, z: !hw.struct<x: i8, y: i1>>, y: i8>, X: i34) {
        %0 = hw.struct_extract %I["x"] : !hw.struct<x: !hw.struct<x: !hw.array<2xi8>, y: i1, z: !hw.struct<x: i8, y: i1>>, y: i8>
        %1 = hw.struct_extract %0["x"] : !hw.struct<x: !hw.array<2xi8>, y: i1, z: !hw.struct<x: i8, y: i1>>
        %3 = hw.constant 0 : i1
        %2 = hw.array_get %1[%3] : !hw.array<2xi8>, i1
        %5 = hw.constant 1 : i1
        %4 = hw.array_get %1[%5] : !hw.array<2xi8>, i1
        %6 = hw.struct_extract %0["y"] : !hw.struct<x: !hw.array<2xi8>, y: i1, z: !hw.struct<x: i8, y: i1>>
        %7 = hw.struct_extract %0["z"] : !hw.struct<x: !hw.array<2xi8>, y: i1, z: !hw.struct<x: i8, y: i1>>
        %9 = hw.array_create %7, %7 : !hw.struct<x: i8, y: i1>
        %8 = hw.array_get %9[%S] : !hw.array<2x!hw.struct<x: i8, y: i1>>, i1
        %10 = hw.struct_extract %I["y"] : !hw.struct<x: !hw.struct<x: !hw.array<2xi8>, y: i1, z: !hw.struct<x: i8, y: i1>>, y: i8>
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
        %75 = hw.array_create %12, %11 : i8
        %76 = hw.struct_create (%75, %13, %14) : !hw.struct<x: !hw.array<2xi8>, y: i1, z: !hw.struct<x: i8, y: i1>>
        %77 = hw.struct_create (%76, %15) : !hw.struct<x: !hw.struct<x: !hw.array<2xi8>, y: i1, z: !hw.struct<x: i8, y: i1>>, y: i8>
        %78 = hw.struct_extract %14["x"] : !hw.struct<x: i8, y: i1>
        %79 = comb.extract %78 from 0 : (i8) -> i1
        %80 = comb.extract %78 from 1 : (i8) -> i1
        %81 = comb.extract %78 from 2 : (i8) -> i1
        %82 = comb.extract %78 from 3 : (i8) -> i1
        %83 = comb.extract %78 from 4 : (i8) -> i1
        %84 = comb.extract %78 from 5 : (i8) -> i1
        %85 = comb.extract %78 from 6 : (i8) -> i1
        %86 = comb.extract %78 from 7 : (i8) -> i1
        %87 = hw.struct_extract %14["y"] : !hw.struct<x: i8, y: i1>
        %88 = comb.extract %11 from 0 : (i8) -> i1
        %89 = comb.extract %11 from 1 : (i8) -> i1
        %90 = comb.extract %11 from 2 : (i8) -> i1
        %91 = comb.extract %11 from 3 : (i8) -> i1
        %92 = comb.extract %11 from 4 : (i8) -> i1
        %93 = comb.extract %11 from 5 : (i8) -> i1
        %94 = comb.extract %11 from 6 : (i8) -> i1
        %95 = comb.extract %11 from 7 : (i8) -> i1
        %96 = comb.extract %12 from 0 : (i8) -> i1
        %97 = comb.extract %12 from 1 : (i8) -> i1
        %98 = comb.extract %12 from 2 : (i8) -> i1
        %99 = comb.extract %12 from 3 : (i8) -> i1
        %100 = comb.extract %12 from 4 : (i8) -> i1
        %101 = comb.extract %12 from 5 : (i8) -> i1
        %102 = comb.extract %12 from 6 : (i8) -> i1
        %103 = comb.extract %12 from 7 : (i8) -> i1
        %104 = comb.extract %15 from 0 : (i8) -> i1
        %105 = comb.extract %15 from 1 : (i8) -> i1
        %106 = comb.extract %15 from 2 : (i8) -> i1
        %107 = comb.extract %15 from 3 : (i8) -> i1
        %108 = comb.extract %15 from 4 : (i8) -> i1
        %109 = comb.extract %15 from 5 : (i8) -> i1
        %110 = comb.extract %15 from 6 : (i8) -> i1
        %111 = comb.extract %15 from 7 : (i8) -> i1
        %112 = comb.concat %111, %110, %109, %108, %107, %106, %105, %104, %103, %102, %101, %100, %99, %98, %97, %96, %95, %94, %93, %92, %91, %90, %89, %88, %87, %86, %85, %84, %83, %82, %81, %80, %79, %13 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        hw.output %77, %112 : !hw.struct<x: !hw.struct<x: !hw.array<2xi8>, y: i1, z: !hw.struct<x: i8, y: i1>>, y: i8>, i34
    }
}
