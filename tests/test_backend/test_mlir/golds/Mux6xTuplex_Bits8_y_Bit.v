module Mux6xTuplex_Bits8_y_Bit(
  input  struct packed {logic [7:0] x; logic y; } I0, I1, I2, I3, I4, I5,
  input  [2:0]                                    S,
  output struct packed {logic [7:0] x; logic y; } O);

  wire [7:0] _T = I0.x;
  wire [7:0] _T_0 = I0.x;
  wire [7:0] _T_1 = I0.x;
  wire [7:0] _T_2 = I0.x;
  wire [7:0] _T_3 = I0.x;
  wire [7:0] _T_4 = I0.x;
  wire [7:0] _T_5 = I0.x;
  wire [7:0] _T_6 = I0.x;
  wire [7:0] _T_7 = I1.x;
  wire [7:0] _T_8 = I1.x;
  wire [7:0] _T_9 = I1.x;
  wire [7:0] _T_10 = I1.x;
  wire [7:0] _T_11 = I1.x;
  wire [7:0] _T_12 = I1.x;
  wire [7:0] _T_13 = I1.x;
  wire [7:0] _T_14 = I1.x;
  wire [7:0] _T_15 = I2.x;
  wire [7:0] _T_16 = I2.x;
  wire [7:0] _T_17 = I2.x;
  wire [7:0] _T_18 = I2.x;
  wire [7:0] _T_19 = I2.x;
  wire [7:0] _T_20 = I2.x;
  wire [7:0] _T_21 = I2.x;
  wire [7:0] _T_22 = I2.x;
  wire [7:0] _T_23 = I3.x;
  wire [7:0] _T_24 = I3.x;
  wire [7:0] _T_25 = I3.x;
  wire [7:0] _T_26 = I3.x;
  wire [7:0] _T_27 = I3.x;
  wire [7:0] _T_28 = I3.x;
  wire [7:0] _T_29 = I3.x;
  wire [7:0] _T_30 = I3.x;
  wire [7:0] _T_31 = I4.x;
  wire [7:0] _T_32 = I4.x;
  wire [7:0] _T_33 = I4.x;
  wire [7:0] _T_34 = I4.x;
  wire [7:0] _T_35 = I4.x;
  wire [7:0] _T_36 = I4.x;
  wire [7:0] _T_37 = I4.x;
  wire [7:0] _T_38 = I4.x;
  wire [7:0] _T_39 = I5.x;
  wire [7:0] _T_40 = I5.x;
  wire [7:0] _T_41 = I5.x;
  wire [7:0] _T_42 = I5.x;
  wire [7:0] _T_43 = I5.x;
  wire [7:0] _T_44 = I5.x;
  wire [7:0] _T_45 = I5.x;
  wire [7:0] _T_46 = I5.x;
  wire [8:0] _tmp = {I5.y, _T_46[7], _T_45[6], _T_44[5], _T_43[4], _T_42[3], _T_41[2], _T_40[1], _T_39[0]};
  wire [8:0] _tmp_50 = {I4.y, _T_38[7], _T_37[6], _T_36[5], _T_35[4], _T_34[3], _T_33[2], _T_32[1], _T_31[0]};
  wire [8:0] _tmp_51 = {I3.y, _T_30[7], _T_29[6], _T_28[5], _T_27[4], _T_26[3], _T_25[2], _T_24[1], _T_23[0]};
  wire [8:0] _tmp_52 = {I2.y, _T_22[7], _T_21[6], _T_20[5], _T_19[4], _T_18[3], _T_17[2], _T_16[1], _T_15[0]};
  wire [8:0] _tmp_53 = {I1.y, _T_14[7], _T_13[6], _T_12[5], _T_11[4], _T_10[3], _T_9[2], _T_8[1], _T_7[0]};
  wire [8:0] _tmp_54 = {I0.y, _T_6[7], _T_5[6], _T_4[5], _T_3[4], _T_2[3], _T_1[2], _T_0[1], _T[0]};
  wire [5:0][8:0] _tmp_55 = {{_tmp}, {_tmp_50}, {_tmp_51}, {_tmp_52}, {_tmp_53}, {_tmp_54}};
  wire struct packed {logic [5:0][8:0] data; logic [2:0] sel; } _T_47 = '{data: _tmp_55, sel: S};
  wire [8:0] _T_48 = _T_47.data[_T_47.sel];
  wire struct packed {logic [7:0] x; logic y; } _T_49 = '{x: (_T_48[7:0]), y: (_T_48[8])};
  assign O = _T_49;
endmodule

