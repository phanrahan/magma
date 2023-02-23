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
        %48 = sv.reg : !hw.inout<i8>
        %8 = sv.read_inout %48 : !hw.inout<i8>
        %49 = sv.reg : !hw.inout<i8>
        %9 = sv.read_inout %49 : !hw.inout<i8>
        %50 = sv.reg : !hw.inout<i1>
        %10 = sv.read_inout %50 : !hw.inout<i1>
        %51 = sv.reg : !hw.inout<i8>
        %11 = sv.read_inout %51 : !hw.inout<i8>
        %52 = sv.reg : !hw.inout<i1>
        %12 = sv.read_inout %52 : !hw.inout<i1>
        %53 = sv.reg : !hw.inout<i8>
        %13 = sv.read_inout %53 : !hw.inout<i8>
        %54 = sv.reg : !hw.inout<i1>
        %14 = sv.read_inout %54 : !hw.inout<i1>
        %55 = sv.reg : !hw.inout<i1>
        %15 = sv.read_inout %55 : !hw.inout<i1>
        %56 = sv.reg : !hw.inout<i1>
        %16 = sv.read_inout %56 : !hw.inout<i1>
        %57 = sv.reg : !hw.inout<i1>
        %17 = sv.read_inout %57 : !hw.inout<i1>
        %58 = sv.reg : !hw.inout<i1>
        %18 = sv.read_inout %58 : !hw.inout<i1>
        %59 = sv.reg : !hw.inout<i1>
        %19 = sv.read_inout %59 : !hw.inout<i1>
        %60 = sv.reg : !hw.inout<i1>
        %20 = sv.read_inout %60 : !hw.inout<i1>
        %61 = sv.reg : !hw.inout<i1>
        %21 = sv.read_inout %61 : !hw.inout<i1>
        %62 = sv.reg : !hw.inout<i1>
        %22 = sv.read_inout %62 : !hw.inout<i1>
        %63 = sv.reg : !hw.inout<i1>
        %23 = sv.read_inout %63 : !hw.inout<i1>
        %64 = sv.reg : !hw.inout<i1>
        %24 = sv.read_inout %64 : !hw.inout<i1>
        %65 = sv.reg : !hw.inout<i1>
        %25 = sv.read_inout %65 : !hw.inout<i1>
        %66 = sv.reg : !hw.inout<i1>
        %26 = sv.read_inout %66 : !hw.inout<i1>
        %67 = sv.reg : !hw.inout<i1>
        %27 = sv.read_inout %67 : !hw.inout<i1>
        %68 = sv.reg : !hw.inout<i1>
        %28 = sv.read_inout %68 : !hw.inout<i1>
        %69 = sv.reg : !hw.inout<i1>
        %29 = sv.read_inout %69 : !hw.inout<i1>
        %70 = sv.reg : !hw.inout<i1>
        %30 = sv.read_inout %70 : !hw.inout<i1>
        %71 = sv.reg : !hw.inout<i1>
        %31 = sv.read_inout %71 : !hw.inout<i1>
        %72 = sv.reg : !hw.inout<i1>
        %32 = sv.read_inout %72 : !hw.inout<i1>
        %73 = sv.reg : !hw.inout<i1>
        %33 = sv.read_inout %73 : !hw.inout<i1>
        %74 = sv.reg : !hw.inout<i1>
        %34 = sv.read_inout %74 : !hw.inout<i1>
        %75 = sv.reg : !hw.inout<i1>
        %35 = sv.read_inout %75 : !hw.inout<i1>
        %76 = sv.reg : !hw.inout<i1>
        %36 = sv.read_inout %76 : !hw.inout<i1>
        %77 = sv.reg : !hw.inout<i1>
        %37 = sv.read_inout %77 : !hw.inout<i1>
        %78 = sv.reg : !hw.inout<i1>
        %38 = sv.read_inout %78 : !hw.inout<i1>
        %79 = sv.reg : !hw.inout<i1>
        %39 = sv.read_inout %79 : !hw.inout<i1>
        %80 = sv.reg : !hw.inout<i1>
        %40 = sv.read_inout %80 : !hw.inout<i1>
        %81 = sv.reg : !hw.inout<i1>
        %41 = sv.read_inout %81 : !hw.inout<i1>
        %82 = sv.reg : !hw.inout<i1>
        %42 = sv.read_inout %82 : !hw.inout<i1>
        %83 = sv.reg : !hw.inout<i1>
        %43 = sv.read_inout %83 : !hw.inout<i1>
        %84 = sv.reg : !hw.inout<i1>
        %44 = sv.read_inout %84 : !hw.inout<i1>
        %85 = sv.reg : !hw.inout<i1>
        %45 = sv.read_inout %85 : !hw.inout<i1>
        %86 = sv.reg : !hw.inout<i1>
        %46 = sv.read_inout %86 : !hw.inout<i1>
        %87 = sv.reg : !hw.inout<i1>
        %47 = sv.read_inout %87 : !hw.inout<i1>
        sv.alwayscomb {
            %96 = comb.concat %95, %94, %93, %92, %91, %90, %89, %88 : i1, i1, i1, i1, i1, i1, i1, i1
            sv.bpassign %53, %96 : i8
            sv.bpassign %80, %88 : i1
            sv.bpassign %81, %89 : i1
            sv.bpassign %82, %90 : i1
            sv.bpassign %83, %91 : i1
            sv.bpassign %84, %92 : i1
            sv.bpassign %85, %93 : i1
            sv.bpassign %86, %94 : i1
            sv.bpassign %87, %95 : i1
            sv.if %S {
                sv.bpassign %50, %I_x_y : i1
                sv.bpassign %54, %I_x_y : i1
                sv.bpassign %52, %5 : i1
                %121 = comb.concat %104, %103, %102, %101, %100, %99, %98, %97 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %51, %121 : i8
                sv.bpassign %55, %97 : i1
                sv.bpassign %56, %98 : i1
                sv.bpassign %57, %99 : i1
                sv.bpassign %58, %100 : i1
                sv.bpassign %59, %101 : i1
                sv.bpassign %60, %102 : i1
                sv.bpassign %61, %103 : i1
                sv.bpassign %62, %104 : i1
                sv.bpassign %63, %5 : i1
                %122 = comb.concat %112, %111, %110, %109, %108, %107, %106, %105 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %48, %122 : i8
                sv.bpassign %64, %105 : i1
                sv.bpassign %65, %106 : i1
                sv.bpassign %66, %107 : i1
                sv.bpassign %67, %108 : i1
                sv.bpassign %68, %109 : i1
                sv.bpassign %69, %110 : i1
                sv.bpassign %70, %111 : i1
                sv.bpassign %71, %112 : i1
                %123 = comb.concat %120, %119, %118, %117, %116, %115, %114, %113 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %49, %123 : i8
                sv.bpassign %72, %113 : i1
                sv.bpassign %73, %114 : i1
                sv.bpassign %74, %115 : i1
                sv.bpassign %75, %116 : i1
                sv.bpassign %76, %117 : i1
                sv.bpassign %77, %118 : i1
                sv.bpassign %78, %119 : i1
                sv.bpassign %79, %120 : i1
            } else {
                sv.bpassign %50, %I_x_y : i1
                sv.bpassign %54, %I_x_y : i1
                sv.bpassign %52, %I_x_z_y : i1
                %132 = comb.concat %131, %130, %129, %128, %127, %126, %125, %124 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %51, %132 : i8
                sv.bpassign %55, %124 : i1
                sv.bpassign %56, %125 : i1
                sv.bpassign %57, %126 : i1
                sv.bpassign %58, %127 : i1
                sv.bpassign %59, %128 : i1
                sv.bpassign %60, %129 : i1
                sv.bpassign %61, %130 : i1
                sv.bpassign %62, %131 : i1
                sv.bpassign %63, %I_x_z_y : i1
                %133 = comb.concat %112, %111, %110, %109, %108, %107, %106, %105 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %48, %133 : i8
                sv.bpassign %64, %105 : i1
                sv.bpassign %65, %106 : i1
                sv.bpassign %66, %107 : i1
                sv.bpassign %67, %108 : i1
                sv.bpassign %68, %109 : i1
                sv.bpassign %69, %110 : i1
                sv.bpassign %70, %111 : i1
                sv.bpassign %71, %112 : i1
                %134 = comb.concat %120, %119, %118, %117, %116, %115, %114, %113 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %49, %134 : i8
                sv.bpassign %72, %113 : i1
                sv.bpassign %73, %114 : i1
                sv.bpassign %74, %115 : i1
                sv.bpassign %75, %116 : i1
                sv.bpassign %76, %117 : i1
                sv.bpassign %77, %118 : i1
                sv.bpassign %78, %119 : i1
                sv.bpassign %79, %120 : i1
                %135 = comb.concat %95, %94, %93, %92, %91, %90, %89, %88 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %53, %135 : i8
                sv.bpassign %80, %88 : i1
                sv.bpassign %81, %89 : i1
                sv.bpassign %82, %90 : i1
                sv.bpassign %83, %91 : i1
                sv.bpassign %84, %92 : i1
                sv.bpassign %85, %93 : i1
                sv.bpassign %86, %94 : i1
                sv.bpassign %87, %95 : i1
            }
        }
        %88 = comb.extract %I_y from 0 : (i8) -> i1
        %89 = comb.extract %I_y from 1 : (i8) -> i1
        %90 = comb.extract %I_y from 2 : (i8) -> i1
        %91 = comb.extract %I_y from 3 : (i8) -> i1
        %92 = comb.extract %I_y from 4 : (i8) -> i1
        %93 = comb.extract %I_y from 5 : (i8) -> i1
        %94 = comb.extract %I_y from 6 : (i8) -> i1
        %95 = comb.extract %I_y from 7 : (i8) -> i1
        %97 = comb.extract %4 from 0 : (i8) -> i1
        %98 = comb.extract %4 from 1 : (i8) -> i1
        %99 = comb.extract %4 from 2 : (i8) -> i1
        %100 = comb.extract %4 from 3 : (i8) -> i1
        %101 = comb.extract %4 from 4 : (i8) -> i1
        %102 = comb.extract %4 from 5 : (i8) -> i1
        %103 = comb.extract %4 from 6 : (i8) -> i1
        %104 = comb.extract %4 from 7 : (i8) -> i1
        %105 = comb.extract %0 from 0 : (i8) -> i1
        %106 = comb.extract %0 from 1 : (i8) -> i1
        %107 = comb.extract %0 from 2 : (i8) -> i1
        %108 = comb.extract %0 from 3 : (i8) -> i1
        %109 = comb.extract %0 from 4 : (i8) -> i1
        %110 = comb.extract %0 from 5 : (i8) -> i1
        %111 = comb.extract %0 from 6 : (i8) -> i1
        %112 = comb.extract %0 from 7 : (i8) -> i1
        %113 = comb.extract %2 from 0 : (i8) -> i1
        %114 = comb.extract %2 from 1 : (i8) -> i1
        %115 = comb.extract %2 from 2 : (i8) -> i1
        %116 = comb.extract %2 from 3 : (i8) -> i1
        %117 = comb.extract %2 from 4 : (i8) -> i1
        %118 = comb.extract %2 from 5 : (i8) -> i1
        %119 = comb.extract %2 from 6 : (i8) -> i1
        %120 = comb.extract %2 from 7 : (i8) -> i1
        %124 = comb.extract %I_x_z_x from 0 : (i8) -> i1
        %125 = comb.extract %I_x_z_x from 1 : (i8) -> i1
        %126 = comb.extract %I_x_z_x from 2 : (i8) -> i1
        %127 = comb.extract %I_x_z_x from 3 : (i8) -> i1
        %128 = comb.extract %I_x_z_x from 4 : (i8) -> i1
        %129 = comb.extract %I_x_z_x from 5 : (i8) -> i1
        %130 = comb.extract %I_x_z_x from 6 : (i8) -> i1
        %131 = comb.extract %I_x_z_x from 7 : (i8) -> i1
        %136 = hw.array_create %9, %8 : i8
        %137 = comb.concat %47, %46, %45, %44, %43, %42, %41, %40, %39, %38, %37, %36, %35, %34, %33, %32, %31, %30, %29, %28, %27, %26, %25, %24, %23, %22, %21, %20, %19, %18, %17, %16, %15, %14 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        hw.output %10, %11, %12, %136, %13, %137 : i1, i8, i1, !hw.array<2xi8>, i8, i34
    }
}
