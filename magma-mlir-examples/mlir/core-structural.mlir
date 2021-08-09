hw.module @Foo(%I: i1) -> (%O: i1) {
  hw.output %I : i1
}

hw.module @Top(%I: i1) -> (%O: i1) {
  %Foo_inst0_O = hw.instance "Foo_inst0" @Foo(%I) : (i1) -> (i1)
  hw.output %Foo_inst0_O : i1
}
