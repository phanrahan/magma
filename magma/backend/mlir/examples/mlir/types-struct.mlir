!Inputs = type !hw.struct<I0: i32, I1: i32, CIN: i1>
!Outputs = type !hw.struct<O: i32, COUT: i1>

hw.module @Top(%I: !Inputs) -> (%O: !Outputs) {
  // "Explode" struct manually using `hw.struct_extract`.
  // NOTE(rsetaluri): Using `hw.struct_explode` for some reason does not
  // succesfully lower to Verilog.
  %0 = hw.struct_extract %I["I0"] : !Inputs
  %1 = hw.struct_extract %I["I1"] : !Inputs
  %2 = hw.struct_extract %I["CIN"] : !Inputs

  // Construct sum operands by zero-extending.
  %zero_1 = hw.constant 0 : i1
  %zero_32 = hw.constant 0 : i32
  %3 = comb.concat %zero_1, %0 : (i1, i32) -> (i33)
  %4 = comb.concat %zero_1, %1 : (i1, i32) -> (i33)
  %5 = comb.concat %zero_32, %2 : (i32, i1) -> (i33)

  // Perform sum.
  %6 = comb.add %3, %4, %5 : i33

  // Extract sum and carry out from from result and re-pack.
  %7 = comb.extract %6 from 0 : (i33) -> (i32)
  %8 = comb.extract %6 from 32 : (i33) -> (i1)
  %9 = hw.struct_create (%7, %8) : !Outputs
  hw.output %9 : !Outputs
}
