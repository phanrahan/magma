hw.module @Mux4xBits8(%I0: i8, %I1: i8, %I2: i8, %I3: i8, %S: i2) -> (%O: i8) {
    %0 = hw.array_create %I3, %I2, %I1, %I0 : i8
    %1 = hw.struct_create (%0, %S) : !hw.struct<data: !hw.array<4xi8>, sel: i2>
    %3 = hw.struct_extract %1["data"] : !hw.struct<data: !hw.array<4xi8>, sel: i2>
    %4 = hw.struct_extract %1["sel"] : !hw.struct<data: !hw.array<4xi8>, sel: i2>
    %2 = hw.array_get %3[%4] : !hw.array<4xi8>
    hw.output %2 : i8
}
