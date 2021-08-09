hw.module @Top2to1(%I0: i4, %I1: i4, %S: i1) -> (%O: i4) {
  %0 = comb.mux %S, %I0, %I1 : i4
  hw.output %0 : i4
}

hw.module @Top8to1(%I0: i4, %I1: i4, %I2: i4, %I3: i4, %I4: i4, %I5: i4, %I6: i4, %I7: i4, %S: i3) -> (%O: i4) {
  %S_0 = comb.extract %S from 0 : (i3) -> i1
  %S_1 = comb.extract %S from 1 : (i3) -> i1
  %S_2 = comb.extract %S from 2 : (i3) -> i1
  %0 = comb.mux %S_0, %I0, %I4 : i4
  %1 = comb.mux %S_0, %I1, %I5 : i4
  %2 = comb.mux %S_0, %I2, %I6 : i4
  %3 = comb.mux %S_0, %I3, %I7 : i4
  %4 = comb.mux %S_1, %0, %2 : i4
  %5 = comb.mux %S_1, %1, %3 : i4
  %6 = comb.mux %S_2, %4, %5 : i4
  hw.output %6 : i4
}
