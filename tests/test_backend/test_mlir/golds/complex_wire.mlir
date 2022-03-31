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
    %16 = comb.extract %13 from 1 : (i32) -> i1
    %17 = comb.extract %13 from 2 : (i32) -> i1
    %18 = comb.extract %13 from 3 : (i32) -> i1
    %19 = comb.extract %13 from 4 : (i32) -> i1
    %20 = comb.extract %13 from 5 : (i32) -> i1
    %21 = comb.extract %13 from 6 : (i32) -> i1
    %22 = comb.extract %13 from 7 : (i32) -> i1
    %23 = hw.array_concat %22, %21, %20, %19, %18, %17, %16, %15 : i1, i1, i1, i1, i1, i1, i1, i1
    %24 = comb.extract %13 from 8 : (i32) -> i1
    %25 = comb.extract %13 from 9 : (i32) -> i1
    %26 = comb.extract %13 from 10 : (i32) -> i1
    %27 = comb.extract %13 from 11 : (i32) -> i1
    %28 = comb.extract %13 from 12 : (i32) -> i1
    %29 = comb.extract %13 from 13 : (i32) -> i1
    %30 = comb.extract %13 from 14 : (i32) -> i1
    %31 = comb.extract %13 from 15 : (i32) -> i1
    %32 = hw.array_concat %31, %30, %29, %28, %27, %26, %25, %24 : i1, i1, i1, i1, i1, i1, i1, i1
    %33 = comb.extract %13 from 16 : (i32) -> i1
    %34 = comb.extract %13 from 17 : (i32) -> i1
    %35 = comb.extract %13 from 18 : (i32) -> i1
    %36 = comb.extract %13 from 19 : (i32) -> i1
    %37 = comb.extract %13 from 20 : (i32) -> i1
    %38 = comb.extract %13 from 21 : (i32) -> i1
    %39 = comb.extract %13 from 22 : (i32) -> i1
    %40 = comb.extract %13 from 23 : (i32) -> i1
    %41 = hw.array_concat %40, %39, %38, %37, %36, %35, %34, %33 : i1, i1, i1, i1, i1, i1, i1, i1
    %42 = comb.extract %13 from 24 : (i32) -> i1
    %43 = comb.extract %13 from 25 : (i32) -> i1
    %44 = comb.extract %13 from 26 : (i32) -> i1
    %45 = comb.extract %13 from 27 : (i32) -> i1
    %46 = comb.extract %13 from 28 : (i32) -> i1
    %47 = comb.extract %13 from 29 : (i32) -> i1
    %48 = comb.extract %13 from 30 : (i32) -> i1
    %49 = comb.extract %13 from 31 : (i32) -> i1
    %50 = hw.array_concat %49, %48, %47, %46, %45, %44, %43, %42 : i1, i1, i1, i1, i1, i1, i1, i1
    %51 = hw.array_concat %50, %41, %32, %23 : i8, i8, i8, i8
    hw.output %0, %2, %51 : i8, i1, !hw.array<4xi8>
}
