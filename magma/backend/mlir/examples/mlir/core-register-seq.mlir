hw.module @Register_8_init_0_rst_0_en(%I: i8, %clk: i1, %rst: i1, %en: i1) -> (%O: i8) {
  %reset_value = hw.constant 0 : i8

  %_reg_I = sv.wire : !hw.inout<i8>
  %reg_I = sv.read_inout %_reg_I : !hw.inout<i8>
  %0 = seq.compreg %reg_I, %clk, %rst, %reset_value {name = "reg"} : i8
  %reg_I_en = comb.mux %en, %I, %0 : i8
  sv.assign %_reg_I, %reg_I_en : i8
  hw.output %0 : i8
}

hw.module @Top(%I: i8, %clk: i1, %rst: i1, %en: i1) -> (%O: i8) {
  %0 = hw.instance "reg0" @Register_8_init_0_rst_0_en(%I, %clk, %rst, %en) : (i8, i1, i1, i1) -> (i8)
  hw.output %0 : i8
}
