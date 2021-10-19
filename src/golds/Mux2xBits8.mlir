hw.module @Mux2xBits8(%I0: i8, %I1: i8, %S: i1) -> (%O: i8) {
    %0 = hw.array_create %I1, %I0 : i8
    %1 = comb.merge %S : i1
    %2 = hw.struct_create (%0, %1) : !hw.struct<data: !hw.array<2xi8>, sel: i1>
    %4 = hw.struct_extract %2["data"] : !hw.struct<data: !hw.array<2xi8>, sel: i1>
    %5 = hw.struct_extract %2["sel"] : !hw.struct<data: !hw.array<2xi8>, sel: i1>
    %3 = hw.array_get %4[%5] : !hw.array<2xi8>
    hw.output %3 : i8
}
