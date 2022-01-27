hw.module @Register_8_init_0_rst_0_en(%I: i8, %clk: i1, %rst: i1, %en: i1) -> (%O: i8) {
  %init_value = hw.constant 0 : i8
  %reset_value = hw.constant 0 : i8

  %reg = sv.reg {name = "reg0"} : !hw.inout<i8>
  sv.initial {
    sv.bpassign %reg, %init_value : i8
  }
  %reg_O = sv.read_inout %reg : !hw.inout<i8>
  %reg_I = comb.mux %en, %I, %reg_O : i8
  sv.alwaysff(posedge %clk) {
    sv.passign %reg, %reg_I : i8
  } (syncreset : posedge %rst) {
    sv.passign %reg, %reset_value : i8
  }
  hw.output %reg_O : i8
}

hw.module @Top(%I: i8, %clk: i1, %rst: i1, %en: i1) -> (%O: i8) {
  %0 = hw.instance "reg0" @Register_8_init_0_rst_0_en(%I, %clk, %rst, %en) : (i8, i1, i1, i1) -> (i8)
  hw.output %0 : i8
}
