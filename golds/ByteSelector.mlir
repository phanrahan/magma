hw.module @Mux2xUInt8(%I0: i8, %I1: i8, %S: i1) -> (%O: i8) {
    %0 = hw.array_create %I1, %I0 : i8
    %1 = hw.struct_create (%0, %S) : !hw.struct<data: !hw.array<2xi8>, sel: i1>
    %2 = hw.struct_extract %1["data"] : !hw.struct<data: !hw.array<2xi8>, sel: i1>
    %3 = hw.struct_extract %1["sel"] : !hw.struct<data: !hw.array<2xi8>, sel: i1>
    %4 = hw.array_get %2[%3] : !hw.array<2xi8>
    hw.output %4 : i8
}
hw.module @ByteSelector(%I: i32, %offset: i2) -> (%O: i8) {
    %0 = hw.constant 0 : i2
    %1 = hw.constant 1 : i2
    %2 = hw.constant 2 : i2
    %3 = comb.extract %I from 24 : (i32) -> i1
    %4 = comb.extract %I from 25 : (i32) -> i1
    %5 = comb.extract %I from 26 : (i32) -> i1
    %6 = comb.extract %I from 27 : (i32) -> i1
    %7 = comb.extract %I from 28 : (i32) -> i1
    %8 = comb.extract %I from 29 : (i32) -> i1
    %9 = comb.extract %I from 30 : (i32) -> i1
    %10 = comb.extract %I from 31 : (i32) -> i1
    %11 = comb.extract %I from 16 : (i32) -> i1
    %12 = comb.extract %I from 17 : (i32) -> i1
    %13 = comb.extract %I from 18 : (i32) -> i1
    %14 = comb.extract %I from 19 : (i32) -> i1
    %15 = comb.extract %I from 20 : (i32) -> i1
    %16 = comb.extract %I from 21 : (i32) -> i1
    %17 = comb.extract %I from 22 : (i32) -> i1
    %18 = comb.extract %I from 23 : (i32) -> i1
    %19 = comb.extract %I from 8 : (i32) -> i1
    %20 = comb.extract %I from 9 : (i32) -> i1
    %21 = comb.extract %I from 10 : (i32) -> i1
    %22 = comb.extract %I from 11 : (i32) -> i1
    %23 = comb.extract %I from 12 : (i32) -> i1
    %24 = comb.extract %I from 13 : (i32) -> i1
    %25 = comb.extract %I from 14 : (i32) -> i1
    %26 = comb.extract %I from 15 : (i32) -> i1
    %27 = comb.extract %I from 0 : (i32) -> i1
    %28 = comb.extract %I from 1 : (i32) -> i1
    %29 = comb.extract %I from 2 : (i32) -> i1
    %30 = comb.extract %I from 3 : (i32) -> i1
    %31 = comb.extract %I from 4 : (i32) -> i1
    %32 = comb.extract %I from 5 : (i32) -> i1
    %33 = comb.extract %I from 6 : (i32) -> i1
    %34 = comb.extract %I from 7 : (i32) -> i1
    %35 = comb.icmp eq %offset, %0 : i2
    %36 = comb.icmp eq %offset, %1 : i2
    %37 = comb.icmp eq %offset, %2 : i2
    %38 = comb.concat %10, %9, %8, %7, %6, %5, %4, %3 : (i1, i1, i1, i1, i1, i1, i1, i1) -> i8
    %39 = comb.concat %18, %17, %16, %15, %14, %13, %12, %11 : (i1, i1, i1, i1, i1, i1, i1, i1) -> i8
    %40 = comb.concat %26, %25, %24, %23, %22, %21, %20, %19 : (i1, i1, i1, i1, i1, i1, i1, i1) -> i8
    %41 = comb.concat %34, %33, %32, %31, %30, %29, %28, %27 : (i1, i1, i1, i1, i1, i1, i1, i1) -> i8
    %42 = hw.instance "Mux2xUInt8_inst0" @Mux2xUInt8(%38, %39, %37) : (i8, i8, i1) -> (i8)
    %43 = hw.instance "Mux2xUInt8_inst1" @Mux2xUInt8(%42, %40, %36) : (i8, i8, i1) -> (i8)
    %44 = hw.instance "Mux2xUInt8_inst2" @Mux2xUInt8(%43, %41, %35) : (i8, i8, i1) -> (i8)
    hw.output %44 : i8
}
