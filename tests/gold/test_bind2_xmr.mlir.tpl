module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @Bottom(in %I: !hw.struct<x: i1, y: i1>, out O: !hw.struct<x: i1, y: i1>, out x: !hw.struct<_0: i1, _1: i8>) {
        %0 = hw.constant 0 : i1
        %1 = hw.constant 0 : i8
        %2 = hw.struct_create (%0, %1) : !hw.struct<_0: i1, _1: i8>
        hw.output %I, %2 : !hw.struct<x: i1, y: i1>, !hw.struct<_0: i1, _1: i8>
    }
    hw.module @Middle(in %I: !hw.struct<x: i1, y: i1>, out O: !hw.struct<x: i1, y: i1>) {
        %0, %1 = hw.instance "bottom" @Bottom(I: %I: !hw.struct<x: i1, y: i1>) -> (O: !hw.struct<x: i1, y: i1>, x: !hw.struct<_0: i1, _1: i8>)
        %2 = hw.struct_extract %I["x"] : !hw.struct<x: i1, y: i1>
        %3 = hw.struct_extract %1["_0"] : !hw.struct<_0: i1, _1: i8>
        hw.output %0 : !hw.struct<x: i1, y: i1>
    }
    hw.module @TopXMRAsserts_mlir(in %I: !hw.struct<x: i1, y: i1>, in %O: !hw.struct<x: i1, y: i1>, in %a: !hw.struct<x: i1, y: i1>, in %b: i1, in %c: i1) attributes {output_filelist = #hw.output_filelist<"$cwd/build/test_bind2_xmr_bind_files.list">} {
        %0 = hw.struct_extract %I["x"] : !hw.struct<x: i1, y: i1>
        %1 = hw.struct_extract %I["y"] : !hw.struct<x: i1, y: i1>
        %2 = hw.struct_extract %O["x"] : !hw.struct<x: i1, y: i1>
        %3 = hw.struct_extract %O["y"] : !hw.struct<x: i1, y: i1>
        %4 = hw.struct_extract %a["x"] : !hw.struct<x: i1, y: i1>
        %5 = hw.struct_extract %a["y"] : !hw.struct<x: i1, y: i1>
    }
    hw.module @Top(in %I: !hw.struct<x: i1, y: i1>, out O: !hw.struct<x: i1, y: i1>) {
        %0 = hw.instance "middle" @Middle(I: %I: !hw.struct<x: i1, y: i1>) -> (O: !hw.struct<x: i1, y: i1>)
        %2 = sv.xmr "middle", "bottom", "O" : !hw.inout<!hw.struct<x: i1, y: i1>>
        %1 = sv.read_inout %2 : !hw.inout<!hw.struct<x: i1, y: i1>>
        %4 = sv.xmr "middle", "bottom", "I.x" : !hw.inout<i1>
        %3 = sv.read_inout %4 : !hw.inout<i1>
        %6 = sv.xmr "middle", "bottom", "x._0" : !hw.inout<i1>
        %5 = sv.read_inout %6 : !hw.inout<i1>
        hw.instance "TopXMRAsserts_mlir_inst0" sym @Top.TopXMRAsserts_mlir_inst0 @TopXMRAsserts_mlir(I: %I: !hw.struct<x: i1, y: i1>, O: %0: !hw.struct<x: i1, y: i1>, a: %1: !hw.struct<x: i1, y: i1>, b: %3: i1, c: %5: i1) -> () {doNotPrint = true}
        hw.output %0 : !hw.struct<x: i1, y: i1>
    }
    sv.bind #hw.innerNameRef<@Top::@Top.TopXMRAsserts_mlir_inst0>
}
