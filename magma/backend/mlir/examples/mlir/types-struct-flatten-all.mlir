hw.module @Top(%I_I0: i32, %I_I1: i32, %I_CIN: i1) -> (%O_O: i32, %O_COUT: i1) {
  // Construct sum operands by zero-extending.
  %zero_1 = hw.constant 0 : i1
  %zero_32 = hw.constant 0 : i32
  %3 = comb.concat %zero_1, %I_I0 : (i1, i32) -> (i33)
  %4 = comb.concat %zero_1, %I_I1 : (i1, i32) -> (i33)
  %5 = comb.concat %zero_32, %I_CIN : (i32, i1) -> (i33)

  // Perform sum.
  %6 = comb.add %3, %4, %5 : i33

  // Extract sum and carry out from from result and re-pack.
  %7 = comb.extract %6 from 0 : (i33) -> (i32)
  %8 = comb.extract %6 from 32 : (i33) -> (i1)

  hw.output %7, %8 : i32, i1
}
