module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @complex_wire(%I0: i8, %I1: i1, %I2: !hw.array<4xi8>) -> (O0: i8, O1: i1, O2: !hw.array<4xi8>) {
        %1 = sv.wire sym @complex_wire.tmp0 {name="tmp0"} : !hw.inout<i8>
        sv.assign %1, %I0 : i8
        %0 = sv.read_inout %1 : !hw.inout<i8>
        %3 = sv.wire sym @complex_wire.tmp1 {name="tmp1"} : !hw.inout<i1>
        sv.assign %3, %I1 : i1
        %2 = sv.read_inout %3 : !hw.inout<i1>
        %5 = hw.constant 0 : i2
        %4 = hw.array_get %I2[%5] : !hw.array<4xi8>, i2
        %6 = comb.extract %4 from 0 : (i8) -> i1
        %7 = comb.extract %4 from 1 : (i8) -> i1
        %8 = comb.extract %4 from 2 : (i8) -> i1
        %9 = comb.extract %4 from 3 : (i8) -> i1
        %10 = comb.extract %4 from 4 : (i8) -> i1
        %11 = comb.extract %4 from 5 : (i8) -> i1
        %12 = comb.extract %4 from 6 : (i8) -> i1
        %13 = comb.extract %4 from 7 : (i8) -> i1
        %15 = hw.constant 1 : i2
        %14 = hw.array_get %I2[%15] : !hw.array<4xi8>, i2
        %16 = comb.extract %14 from 0 : (i8) -> i1
        %17 = comb.extract %14 from 1 : (i8) -> i1
        %18 = comb.extract %14 from 2 : (i8) -> i1
        %19 = comb.extract %14 from 3 : (i8) -> i1
        %20 = comb.extract %14 from 4 : (i8) -> i1
        %21 = comb.extract %14 from 5 : (i8) -> i1
        %22 = comb.extract %14 from 6 : (i8) -> i1
        %23 = comb.extract %14 from 7 : (i8) -> i1
        %25 = hw.constant 2 : i2
        %24 = hw.array_get %I2[%25] : !hw.array<4xi8>, i2
        %26 = comb.extract %24 from 0 : (i8) -> i1
        %27 = comb.extract %24 from 1 : (i8) -> i1
        %28 = comb.extract %24 from 2 : (i8) -> i1
        %29 = comb.extract %24 from 3 : (i8) -> i1
        %30 = comb.extract %24 from 4 : (i8) -> i1
        %31 = comb.extract %24 from 5 : (i8) -> i1
        %32 = comb.extract %24 from 6 : (i8) -> i1
        %33 = comb.extract %24 from 7 : (i8) -> i1
        %35 = hw.constant 3 : i2
        %34 = hw.array_get %I2[%35] : !hw.array<4xi8>, i2
        %36 = comb.extract %34 from 0 : (i8) -> i1
        %37 = comb.extract %34 from 1 : (i8) -> i1
        %38 = comb.extract %34 from 2 : (i8) -> i1
        %39 = comb.extract %34 from 3 : (i8) -> i1
        %40 = comb.extract %34 from 4 : (i8) -> i1
        %41 = comb.extract %34 from 5 : (i8) -> i1
        %42 = comb.extract %34 from 6 : (i8) -> i1
        %43 = comb.extract %34 from 7 : (i8) -> i1
        %44 = comb.concat %43, %42, %41, %40, %39, %38, %37, %36, %33, %32, %31, %30, %29, %28, %27, %26, %23, %22, %21, %20, %19, %18, %17, %16, %13, %12, %11, %10, %9, %8, %7, %6 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        %46 = sv.wire sym @complex_wire.tmp2 {name="tmp2"} : !hw.inout<i32>
        sv.assign %46, %44 : i32
        %45 = sv.read_inout %46 : !hw.inout<i32>
        %47 = comb.extract %45 from 0 : (i32) -> i1
        %48 = comb.extract %45 from 1 : (i32) -> i1
        %49 = comb.extract %45 from 2 : (i32) -> i1
        %50 = comb.extract %45 from 3 : (i32) -> i1
        %51 = comb.extract %45 from 4 : (i32) -> i1
        %52 = comb.extract %45 from 5 : (i32) -> i1
        %53 = comb.extract %45 from 6 : (i32) -> i1
        %54 = comb.extract %45 from 7 : (i32) -> i1
        %55 = comb.concat %54, %53, %52, %51, %50, %49, %48, %47 : i1, i1, i1, i1, i1, i1, i1, i1
        %56 = comb.extract %45 from 8 : (i32) -> i1
        %57 = comb.extract %45 from 9 : (i32) -> i1
        %58 = comb.extract %45 from 10 : (i32) -> i1
        %59 = comb.extract %45 from 11 : (i32) -> i1
        %60 = comb.extract %45 from 12 : (i32) -> i1
        %61 = comb.extract %45 from 13 : (i32) -> i1
        %62 = comb.extract %45 from 14 : (i32) -> i1
        %63 = comb.extract %45 from 15 : (i32) -> i1
        %64 = comb.concat %63, %62, %61, %60, %59, %58, %57, %56 : i1, i1, i1, i1, i1, i1, i1, i1
        %65 = comb.extract %45 from 16 : (i32) -> i1
        %66 = comb.extract %45 from 17 : (i32) -> i1
        %67 = comb.extract %45 from 18 : (i32) -> i1
        %68 = comb.extract %45 from 19 : (i32) -> i1
        %69 = comb.extract %45 from 20 : (i32) -> i1
        %70 = comb.extract %45 from 21 : (i32) -> i1
        %71 = comb.extract %45 from 22 : (i32) -> i1
        %72 = comb.extract %45 from 23 : (i32) -> i1
        %73 = comb.concat %72, %71, %70, %69, %68, %67, %66, %65 : i1, i1, i1, i1, i1, i1, i1, i1
        %74 = comb.extract %45 from 24 : (i32) -> i1
        %75 = comb.extract %45 from 25 : (i32) -> i1
        %76 = comb.extract %45 from 26 : (i32) -> i1
        %77 = comb.extract %45 from 27 : (i32) -> i1
        %78 = comb.extract %45 from 28 : (i32) -> i1
        %79 = comb.extract %45 from 29 : (i32) -> i1
        %80 = comb.extract %45 from 30 : (i32) -> i1
        %81 = comb.extract %45 from 31 : (i32) -> i1
        %82 = comb.concat %81, %80, %79, %78, %77, %76, %75, %74 : i1, i1, i1, i1, i1, i1, i1, i1
        %83 = hw.array_create %82, %73, %64, %55 : i8
        hw.output %0, %2, %83 : i8, i1, !hw.array<4xi8>
    }
}
