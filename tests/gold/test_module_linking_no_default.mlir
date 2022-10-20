module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @_OrImpl(%I0: i1, %I1: i1) -> (O: i1) {
        %0 = comb.or %I0, %I1 : i1
        hw.output %0 : i1
    }
    hw.module @_AndImpl(%I0: i1, %I1: i1) -> (O: i1) {
        %0 = comb.and %I0, %I1 : i1
        hw.output %0 : i1
    }
    hw.module @_BinOpInterface(%I0: i1, %I1: i1) -> (O: i1) {
        %1 = sv.wire : !hw.inout<i1>
        %0 = sv.read_inout %1 : !hw.inout<i1>
        sv.ifdef "OR" {
            %2 = hw.instance "_OrImpl_inst" @_OrImpl(I0: %I0: i1, I1: %I1: i1) -> (O: i1)
            sv.assign %1, %2 : i1
        } else {
            sv.ifdef "AND" {
                %3 = hw.instance "_AndImpl_inst" @_AndImpl(I0: %I0: i1, I1: %I1: i1) -> (O: i1)
                sv.assign %1, %3 : i1
            } else {
            }
        }
        hw.output %0 : i1
    }
    hw.module @_Top(%I0: i1, %I1: i1) -> (O: i1) {
        %0 = hw.instance "_BinOpInterface_inst0" @_BinOpInterface(I0: %I0: i1, I1: %I1: i1) -> (O: i1)
        hw.output %0 : i1
    }
}
