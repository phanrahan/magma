hw.module @Top(%I: i64) -> (%O16_0: i16, %O32_0: i32) {
  %I16_0 = comb.extract %I from 16 : (i64) -> i16
  %I16_1 = comb.extract %I from 32 : (i64) -> i16
  %I24_0 = comb.extract %I from 20 : (i64) -> i24
  %I32_0 = comb.extract %I from 24 : (i64) -> i32
  
  %0 = comb.and %I16_0, %I16_1 : i16
  %1 = comb.add %0, %I16_0 : i16
  %2 = comb.mul %1, %I16_1 : i16

  hw.output %2, %I32_0 : i16, i32
}
