hw.module @Mux2xBits8(%I0: i8, %I1: i8, %S: i1) -> (%O: i8) {
    %0 = hw.array_create %I1, %I0 : i8
    %1 = hw.struct_create (%0, %S) : !hw.struct<data: !hw.array<2xi8>, sel: i1>
    %2 = hw.struct_extract %1["data"] : !hw.struct<data: !hw.array<2xi8>, sel: i1>
    %3 = hw.struct_extract %1["sel"] : !hw.struct<data: !hw.array<2xi8>, sel: i1>
    %4 = hw.array_get %2[%3] : !hw.array<2xi8>
    hw.output %4 : i8
}
