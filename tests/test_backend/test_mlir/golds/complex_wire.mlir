hw.module @complex_wire(%I0: i8, %I1: i1, %I2: !hw.array<4xi8>) -> (O0: i8, O1: i1, O2: !hw.array<4xi8>) {
    %1 = sv.wire sym @complex_wire.tmp0 {name="tmp0"} : !hw.inout<i8>
    sv.assign %1, %I0 : i8
    %0 = sv.read_inout %1 : !hw.inout<i8>
    %3 = sv.wire sym @complex_wire.tmp1 {name="tmp1"} : !hw.inout<i1>
    sv.assign %3, %I1 : i1
    %2 = sv.read_inout %3 : !hw.inout<i1>
    %5 = hw.constant 0 : i2
    %4 = hw.array_get %I2[%5] : !hw.array<4xi8>
    %7 = hw.constant 1 : i2
    %6 = hw.array_get %I2[%7] : !hw.array<4xi8>
    %9 = hw.constant 2 : i2
    %8 = hw.array_get %I2[%9] : !hw.array<4xi8>
    %11 = hw.constant 3 : i2
    %10 = hw.array_get %I2[%11] : !hw.array<4xi8>
    %12 = hw.array_concat %10, %8, %6, %4 : i8, i8, i8, i8
    %14 = sv.wire sym @complex_wire.tmp2 {name="tmp2"} : !hw.inout<i32>
    sv.assign %14, %12 : i32
    %13 = sv.read_inout %14 : !hw.inout<i32>
    %15 = comb.extract %13 from 0 : (i32) -> i1
    %16 = comb.concat %15 : i1
    %17 = comb.extract %13 from 1 : (i32) -> i1
    %18 = comb.concat %17 : i1
    %19 = comb.extract %13 from 2 : (i32) -> i1
    %20 = comb.concat %19 : i1
    %21 = comb.extract %13 from 3 : (i32) -> i1
    %22 = comb.concat %21 : i1
    %23 = comb.extract %13 from 4 : (i32) -> i1
    %24 = comb.concat %23 : i1
    %25 = comb.extract %13 from 5 : (i32) -> i1
    %26 = comb.concat %25 : i1
    %27 = comb.extract %13 from 6 : (i32) -> i1
    %28 = comb.concat %27 : i1
    %29 = comb.extract %13 from 7 : (i32) -> i1
    %30 = comb.concat %29 : i1
    %31 = hw.array_concat %30, %28, %26, %24, %22, %20, %18, %16 : i1, i1, i1, i1, i1, i1, i1, i1
    %32 = hw.array_create %31 : i8
    %33 = comb.extract %13 from 8 : (i32) -> i1
    %34 = comb.concat %33 : i1
    %35 = comb.extract %13 from 9 : (i32) -> i1
    %36 = comb.concat %35 : i1
    %37 = comb.extract %13 from 10 : (i32) -> i1
    %38 = comb.concat %37 : i1
    %39 = comb.extract %13 from 11 : (i32) -> i1
    %40 = comb.concat %39 : i1
    %41 = comb.extract %13 from 12 : (i32) -> i1
    %42 = comb.concat %41 : i1
    %43 = comb.extract %13 from 13 : (i32) -> i1
    %44 = comb.concat %43 : i1
    %45 = comb.extract %13 from 14 : (i32) -> i1
    %46 = comb.concat %45 : i1
    %47 = comb.extract %13 from 15 : (i32) -> i1
    %48 = comb.concat %47 : i1
    %49 = hw.array_concat %48, %46, %44, %42, %40, %38, %36, %34 : i1, i1, i1, i1, i1, i1, i1, i1
    %50 = hw.array_create %49 : i8
    %51 = comb.extract %13 from 16 : (i32) -> i1
    %52 = comb.concat %51 : i1
    %53 = comb.extract %13 from 17 : (i32) -> i1
    %54 = comb.concat %53 : i1
    %55 = comb.extract %13 from 18 : (i32) -> i1
    %56 = comb.concat %55 : i1
    %57 = comb.extract %13 from 19 : (i32) -> i1
    %58 = comb.concat %57 : i1
    %59 = comb.extract %13 from 20 : (i32) -> i1
    %60 = comb.concat %59 : i1
    %61 = comb.extract %13 from 21 : (i32) -> i1
    %62 = comb.concat %61 : i1
    %63 = comb.extract %13 from 22 : (i32) -> i1
    %64 = comb.concat %63 : i1
    %65 = comb.extract %13 from 23 : (i32) -> i1
    %66 = comb.concat %65 : i1
    %67 = hw.array_concat %66, %64, %62, %60, %58, %56, %54, %52 : i1, i1, i1, i1, i1, i1, i1, i1
    %68 = hw.array_create %67 : i8
    %69 = comb.extract %13 from 24 : (i32) -> i1
    %70 = comb.concat %69 : i1
    %71 = comb.extract %13 from 25 : (i32) -> i1
    %72 = comb.concat %71 : i1
    %73 = comb.extract %13 from 26 : (i32) -> i1
    %74 = comb.concat %73 : i1
    %75 = comb.extract %13 from 27 : (i32) -> i1
    %76 = comb.concat %75 : i1
    %77 = comb.extract %13 from 28 : (i32) -> i1
    %78 = comb.concat %77 : i1
    %79 = comb.extract %13 from 29 : (i32) -> i1
    %80 = comb.concat %79 : i1
    %81 = comb.extract %13 from 30 : (i32) -> i1
    %82 = comb.concat %81 : i1
    %83 = comb.extract %13 from 31 : (i32) -> i1
    %84 = comb.concat %83 : i1
    %85 = hw.array_concat %84, %82, %80, %78, %76, %74, %72, %70 : i1, i1, i1, i1, i1, i1, i1, i1
    %86 = hw.array_create %85 : i8
    %87 = hw.array_concat %86, %68, %50, %32 : !hw.array<1xi8>, !hw.array<1xi8>, !hw.array<1xi8>, !hw.array<1xi8>
    hw.output %0, %2, %87 : i8, i1, !hw.array<4xi8>
}
