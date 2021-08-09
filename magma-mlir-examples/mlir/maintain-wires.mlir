hw.module @Top(%I0: i1, %I1: i1) -> (%O: i1) {
  %x = sv.wire sym @_0 : !hw.inout<i1>
  %0 = comb.or %I0, %I1 : i1
  sv.assign %x, %0 : i1
  %x_o = sv.read_inout %x : !hw.inout<i1>
  hw.output %x_o : i1
}
