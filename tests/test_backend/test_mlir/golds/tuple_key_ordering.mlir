module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @tuple_key_ordering(%I: !hw.struct<x: i1, y: i8>) -> (O: !hw.struct<x: i1, y: i8>) {
        hw.output %I : !hw.struct<x: i1, y: i8>
    }
}
