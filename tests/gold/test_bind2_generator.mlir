module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @LogicAsserts(%I: i1, %O: i1, %other: i1) -> () {
        %1 = sv.wire sym @LogicAsserts._magma_inline_wire0 {name="_magma_inline_wire0"} : !hw.inout<i1>
        sv.assign %1, %I : i1
        %0 = sv.read_inout %1 : !hw.inout<i1>
        %3 = sv.wire sym @LogicAsserts._magma_inline_wire1 {name="_magma_inline_wire1"} : !hw.inout<i1>
        sv.assign %3, %O : i1
        %2 = sv.read_inout %3 : !hw.inout<i1>
        %5 = sv.wire sym @LogicAsserts._magma_inline_wire2 {name="_magma_inline_wire2"} : !hw.inout<i1>
        sv.assign %5, %other : i1
        %4 = sv.read_inout %5 : !hw.inout<i1>
        sv.verbatim "{{0}} {{1}} {{2}}" (%0, %2, %4) : i1, i1, i1
    }
    hw.module @Logic(%I: i1) -> (O: i1) {
        %1 = hw.constant -1 : i1
        %0 = comb.xor %1, %I : i1
        hw.instance "LogicAsserts_inst0" sym @Logic.LogicAsserts_inst0 @LogicAsserts(I: %I: i1, O: %0: i1, other: %I: i1) -> () {doNotPrint = 1}
        hw.output %0 : i1
    }
    sv.bind #hw.innerNameRef<@Logic::@Logic.LogicAsserts_inst0>
    hw.module @LogicAsserts_unq1(%I: i2, %O: i2, %other: i1) -> () {
        %1 = sv.wire sym @LogicAsserts_unq1._magma_inline_wire0 {name="_magma_inline_wire0"} : !hw.inout<i2>
        sv.assign %1, %I : i2
        %0 = sv.read_inout %1 : !hw.inout<i2>
        %3 = sv.wire sym @LogicAsserts_unq1._magma_inline_wire1 {name="_magma_inline_wire1"} : !hw.inout<i2>
        sv.assign %3, %O : i2
        %2 = sv.read_inout %3 : !hw.inout<i2>
        %5 = sv.wire sym @LogicAsserts_unq1._magma_inline_wire2 {name="_magma_inline_wire2"} : !hw.inout<i1>
        sv.assign %5, %other : i1
        %4 = sv.read_inout %5 : !hw.inout<i1>
        sv.verbatim "{{0}} {{1}} {{2}}" (%0, %2, %4) : i2, i2, i1
    }
    hw.module @Logic_unq1(%I: i2) -> (O: i2) {
        %1 = hw.constant -1 : i2
        %0 = comb.xor %1, %I : i2
        %2 = comb.extract %I from 0 : (i2) -> i1
        hw.instance "LogicAsserts_inst0" sym @Logic_unq1.LogicAsserts_inst0 @LogicAsserts_unq1(I: %I: i2, O: %0: i2, other: %2: i1) -> () {doNotPrint = 1}
        hw.output %0 : i2
    }
    sv.bind #hw.innerNameRef<@Logic_unq1::@Logic_unq1.LogicAsserts_inst0>
    hw.module @Top(%I: i2) -> (O: i2) {
        %0 = comb.extract %I from 0 : (i2) -> i1
        %1 = hw.instance "Logic_inst0" @Logic(I: %0: i1) -> (O: i1)
        %2 = comb.extract %I from 1 : (i2) -> i1
        %3 = hw.instance "Logic_inst1" @Logic(I: %2: i1) -> (O: i1)
        %4 = comb.concat %3, %1 : i1, i1
        %5 = hw.instance "Logic_inst2" @Logic_unq1(I: %4: i2) -> (O: i2)
        hw.output %5 : i2
    }
}
