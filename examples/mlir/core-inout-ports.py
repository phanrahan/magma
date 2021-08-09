hw.module @Foo(%I: !hw.inout<i1>, %O: !hw.inout<i1>) {
    %_O = sv.read_inout %O : !hw.inout<i1>
    sv.assign %I, %_O : i1
}

hw.module @Top(%I: !hw.inout<i1>, %O: !hw.inout<i1>) {
    %0 = sv.wire {name = "foo1_O"} : !hw.inout<i1>
    hw.instance "foo0" @Foo(%I, %0) : (!hw.inout<i1>, !hw.inout<i1>) -> ()
    hw.instance "foo1" @Foo(%O, %0) : (!hw.inout<i1>, !hw.inout<i1>) -> ()
}
