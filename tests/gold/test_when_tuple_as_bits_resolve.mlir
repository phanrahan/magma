module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_tuple_as_bits_resolve(%I_x_x: !hw.array<2xi8>, %I_x_y: i1, %I_x_z: i8, %S: i1) -> (O_x_x: !hw.array<2xi8>, O_x_y: i1, O_x_z: i8, X: i25) {
        %1 = hw.constant 0 : i1
        %0 = hw.array_get %I_x_x[%1] : !hw.array<2xi8>, i1
        %3 = hw.constant 1 : i1
        %2 = hw.array_get %I_x_x[%3] : !hw.array<2xi8>, i1
        %5 = hw.constant -1 : i8
        %4 = comb.xor %5, %0 : i8
        %6 = comb.xor %5, %2 : i8
        %8 = hw.constant -1 : i1
        %7 = comb.xor %8, %I_x_y : i1
        %9 = comb.xor %5, %I_x_z : i8
        %39 = sv.reg : !hw.inout<i8>
        %10 = sv.read_inout %39 : !hw.inout<i8>
        %40 = sv.reg : !hw.inout<i8>
        %11 = sv.read_inout %40 : !hw.inout<i8>
        %41 = sv.reg : !hw.inout<i1>
        %12 = sv.read_inout %41 : !hw.inout<i1>
        %42 = sv.reg : !hw.inout<i8>
        %13 = sv.read_inout %42 : !hw.inout<i8>
        %43 = sv.reg : !hw.inout<i1>
        %14 = sv.read_inout %43 : !hw.inout<i1>
        %44 = sv.reg : !hw.inout<i1>
        %15 = sv.read_inout %44 : !hw.inout<i1>
        %45 = sv.reg : !hw.inout<i1>
        %16 = sv.read_inout %45 : !hw.inout<i1>
        %46 = sv.reg : !hw.inout<i1>
        %17 = sv.read_inout %46 : !hw.inout<i1>
        %47 = sv.reg : !hw.inout<i1>
        %18 = sv.read_inout %47 : !hw.inout<i1>
        %48 = sv.reg : !hw.inout<i1>
        %19 = sv.read_inout %48 : !hw.inout<i1>
        %49 = sv.reg : !hw.inout<i1>
        %20 = sv.read_inout %49 : !hw.inout<i1>
        %50 = sv.reg : !hw.inout<i1>
        %21 = sv.read_inout %50 : !hw.inout<i1>
        %51 = sv.reg : !hw.inout<i1>
        %22 = sv.read_inout %51 : !hw.inout<i1>
        %52 = sv.reg : !hw.inout<i1>
        %23 = sv.read_inout %52 : !hw.inout<i1>
        %53 = sv.reg : !hw.inout<i1>
        %24 = sv.read_inout %53 : !hw.inout<i1>
        %54 = sv.reg : !hw.inout<i1>
        %25 = sv.read_inout %54 : !hw.inout<i1>
        %55 = sv.reg : !hw.inout<i1>
        %26 = sv.read_inout %55 : !hw.inout<i1>
        %56 = sv.reg : !hw.inout<i1>
        %27 = sv.read_inout %56 : !hw.inout<i1>
        %57 = sv.reg : !hw.inout<i1>
        %28 = sv.read_inout %57 : !hw.inout<i1>
        %58 = sv.reg : !hw.inout<i1>
        %29 = sv.read_inout %58 : !hw.inout<i1>
        %59 = sv.reg : !hw.inout<i1>
        %30 = sv.read_inout %59 : !hw.inout<i1>
        %60 = sv.reg : !hw.inout<i1>
        %31 = sv.read_inout %60 : !hw.inout<i1>
        %61 = sv.reg : !hw.inout<i1>
        %32 = sv.read_inout %61 : !hw.inout<i1>
        %62 = sv.reg : !hw.inout<i1>
        %33 = sv.read_inout %62 : !hw.inout<i1>
        %63 = sv.reg : !hw.inout<i1>
        %34 = sv.read_inout %63 : !hw.inout<i1>
        %64 = sv.reg : !hw.inout<i1>
        %35 = sv.read_inout %64 : !hw.inout<i1>
        %65 = sv.reg : !hw.inout<i1>
        %36 = sv.read_inout %65 : !hw.inout<i1>
        %66 = sv.reg : !hw.inout<i1>
        %37 = sv.read_inout %66 : !hw.inout<i1>
        %67 = sv.reg : !hw.inout<i1>
        %38 = sv.read_inout %67 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %41, %I_x_y : i1
                %92 = comb.concat %75, %74, %73, %72, %71, %70, %69, %68 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %39, %92 : i8
                sv.bpassign %43, %68 : i1
                sv.bpassign %44, %69 : i1
                sv.bpassign %45, %70 : i1
                sv.bpassign %46, %71 : i1
                sv.bpassign %47, %72 : i1
                sv.bpassign %48, %73 : i1
                sv.bpassign %49, %74 : i1
                sv.bpassign %50, %75 : i1
                %93 = comb.concat %83, %82, %81, %80, %79, %78, %77, %76 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %40, %93 : i8
                sv.bpassign %51, %76 : i1
                sv.bpassign %52, %77 : i1
                sv.bpassign %53, %78 : i1
                sv.bpassign %54, %79 : i1
                sv.bpassign %55, %80 : i1
                sv.bpassign %56, %81 : i1
                sv.bpassign %57, %82 : i1
                sv.bpassign %58, %83 : i1
                sv.bpassign %59, %I_x_y : i1
                %94 = comb.concat %91, %90, %89, %88, %87, %86, %85, %84 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %42, %94 : i8
                sv.bpassign %60, %84 : i1
                sv.bpassign %61, %85 : i1
                sv.bpassign %62, %86 : i1
                sv.bpassign %63, %87 : i1
                sv.bpassign %64, %88 : i1
                sv.bpassign %65, %89 : i1
                sv.bpassign %66, %90 : i1
                sv.bpassign %67, %91 : i1
            } else {
                sv.bpassign %41, %7 : i1
                %119 = comb.concat %102, %101, %100, %99, %98, %97, %96, %95 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %39, %119 : i8
                sv.bpassign %43, %95 : i1
                sv.bpassign %44, %96 : i1
                sv.bpassign %45, %97 : i1
                sv.bpassign %46, %98 : i1
                sv.bpassign %47, %99 : i1
                sv.bpassign %48, %100 : i1
                sv.bpassign %49, %101 : i1
                sv.bpassign %50, %102 : i1
                %120 = comb.concat %110, %109, %108, %107, %106, %105, %104, %103 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %40, %120 : i8
                sv.bpassign %51, %103 : i1
                sv.bpassign %52, %104 : i1
                sv.bpassign %53, %105 : i1
                sv.bpassign %54, %106 : i1
                sv.bpassign %55, %107 : i1
                sv.bpassign %56, %108 : i1
                sv.bpassign %57, %109 : i1
                sv.bpassign %58, %110 : i1
                sv.bpassign %59, %7 : i1
                %121 = comb.concat %118, %117, %116, %115, %114, %113, %112, %111 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %42, %121 : i8
                sv.bpassign %60, %111 : i1
                sv.bpassign %61, %112 : i1
                sv.bpassign %62, %113 : i1
                sv.bpassign %63, %114 : i1
                sv.bpassign %64, %115 : i1
                sv.bpassign %65, %116 : i1
                sv.bpassign %66, %117 : i1
                sv.bpassign %67, %118 : i1
            }
        }
        %68 = comb.extract %0 from 0 : (i8) -> i1
        %69 = comb.extract %0 from 1 : (i8) -> i1
        %70 = comb.extract %0 from 2 : (i8) -> i1
        %71 = comb.extract %0 from 3 : (i8) -> i1
        %72 = comb.extract %0 from 4 : (i8) -> i1
        %73 = comb.extract %0 from 5 : (i8) -> i1
        %74 = comb.extract %0 from 6 : (i8) -> i1
        %75 = comb.extract %0 from 7 : (i8) -> i1
        %76 = comb.extract %2 from 0 : (i8) -> i1
        %77 = comb.extract %2 from 1 : (i8) -> i1
        %78 = comb.extract %2 from 2 : (i8) -> i1
        %79 = comb.extract %2 from 3 : (i8) -> i1
        %80 = comb.extract %2 from 4 : (i8) -> i1
        %81 = comb.extract %2 from 5 : (i8) -> i1
        %82 = comb.extract %2 from 6 : (i8) -> i1
        %83 = comb.extract %2 from 7 : (i8) -> i1
        %84 = comb.extract %I_x_z from 0 : (i8) -> i1
        %85 = comb.extract %I_x_z from 1 : (i8) -> i1
        %86 = comb.extract %I_x_z from 2 : (i8) -> i1
        %87 = comb.extract %I_x_z from 3 : (i8) -> i1
        %88 = comb.extract %I_x_z from 4 : (i8) -> i1
        %89 = comb.extract %I_x_z from 5 : (i8) -> i1
        %90 = comb.extract %I_x_z from 6 : (i8) -> i1
        %91 = comb.extract %I_x_z from 7 : (i8) -> i1
        %95 = comb.extract %4 from 0 : (i8) -> i1
        %96 = comb.extract %4 from 1 : (i8) -> i1
        %97 = comb.extract %4 from 2 : (i8) -> i1
        %98 = comb.extract %4 from 3 : (i8) -> i1
        %99 = comb.extract %4 from 4 : (i8) -> i1
        %100 = comb.extract %4 from 5 : (i8) -> i1
        %101 = comb.extract %4 from 6 : (i8) -> i1
        %102 = comb.extract %4 from 7 : (i8) -> i1
        %103 = comb.extract %6 from 0 : (i8) -> i1
        %104 = comb.extract %6 from 1 : (i8) -> i1
        %105 = comb.extract %6 from 2 : (i8) -> i1
        %106 = comb.extract %6 from 3 : (i8) -> i1
        %107 = comb.extract %6 from 4 : (i8) -> i1
        %108 = comb.extract %6 from 5 : (i8) -> i1
        %109 = comb.extract %6 from 6 : (i8) -> i1
        %110 = comb.extract %6 from 7 : (i8) -> i1
        %111 = comb.extract %9 from 0 : (i8) -> i1
        %112 = comb.extract %9 from 1 : (i8) -> i1
        %113 = comb.extract %9 from 2 : (i8) -> i1
        %114 = comb.extract %9 from 3 : (i8) -> i1
        %115 = comb.extract %9 from 4 : (i8) -> i1
        %116 = comb.extract %9 from 5 : (i8) -> i1
        %117 = comb.extract %9 from 6 : (i8) -> i1
        %118 = comb.extract %9 from 7 : (i8) -> i1
        %122 = hw.array_create %11, %10 : i8
        %123 = comb.concat %38, %37, %36, %35, %34, %33, %32, %31, %30, %29, %28, %27, %26, %25, %24, %23, %22, %21, %20, %19, %18, %17, %16, %15, %14 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        hw.output %122, %12, %13, %123 : !hw.array<2xi8>, i1, i8, i25
    }
}
