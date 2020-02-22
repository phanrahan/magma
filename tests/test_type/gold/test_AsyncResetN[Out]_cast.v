// Module `Inst` defined externally
module coreir_wrap (
    input in,
    output out
);
  assign out = in;
endmodule

module AsyncResetTest (
    output [3:0] Bit_Arr_out,
    output Bit_out,
    input I,
    input [2:0] I_Arr,
    output O,
    output [1:0] O_Arr,
    output O_Tuple_B,
    output O_Tuple_R,
    input [1:0] T_Arr_in,
    input T_Tuple_in_T,
    input T_in
);
wire Inst_inst0_O;
wire coreir_wrapInAsyncResetN_inst0_out;
wire coreir_wrapInAsyncResetN_inst1_out;
wire coreir_wrapInAsyncResetN_inst2_out;
wire coreir_wrapInAsyncResetN_inst3_out;
wire coreir_wrapInAsyncResetN_inst4_out;
wire coreir_wrapInAsyncResetN_inst5_out;
wire coreir_wrapOutAsyncResetN_inst0_out;
wire coreir_wrapOutAsyncResetN_inst1_out;
wire coreir_wrapOutAsyncResetN_inst2_out;
wire coreir_wrapOutAsyncResetN_inst3_out;
wire coreir_wrapOutAsyncResetN_inst4_out;
Inst Inst_inst0 (
    .O(Inst_inst0_O),
    .I(coreir_wrapOutAsyncResetN_inst0_out)
);
coreir_wrap coreir_wrapInAsyncResetN_inst0 (
    .in(T_Tuple_in_T),
    .out(coreir_wrapInAsyncResetN_inst0_out)
);
coreir_wrap coreir_wrapInAsyncResetN_inst1 (
    .in(T_in),
    .out(coreir_wrapInAsyncResetN_inst1_out)
);
coreir_wrap coreir_wrapInAsyncResetN_inst2 (
    .in(T_Arr_in[0]),
    .out(coreir_wrapInAsyncResetN_inst2_out)
);
coreir_wrap coreir_wrapInAsyncResetN_inst3 (
    .in(T_Arr_in[1]),
    .out(coreir_wrapInAsyncResetN_inst3_out)
);
coreir_wrap coreir_wrapInAsyncResetN_inst4 (
    .in(T_Arr_in[0]),
    .out(coreir_wrapInAsyncResetN_inst4_out)
);
coreir_wrap coreir_wrapInAsyncResetN_inst5 (
    .in(Inst_inst0_O),
    .out(coreir_wrapInAsyncResetN_inst5_out)
);
coreir_wrap coreir_wrapOutAsyncResetN_inst0 (
    .in(I_Arr[2]),
    .out(coreir_wrapOutAsyncResetN_inst0_out)
);
coreir_wrap coreir_wrapOutAsyncResetN_inst1 (
    .in(I),
    .out(coreir_wrapOutAsyncResetN_inst1_out)
);
coreir_wrap coreir_wrapOutAsyncResetN_inst2 (
    .in(I_Arr[0]),
    .out(coreir_wrapOutAsyncResetN_inst2_out)
);
coreir_wrap coreir_wrapOutAsyncResetN_inst3 (
    .in(I_Arr[1]),
    .out(coreir_wrapOutAsyncResetN_inst3_out)
);
coreir_wrap coreir_wrapOutAsyncResetN_inst4 (
    .in(I_Arr[2]),
    .out(coreir_wrapOutAsyncResetN_inst4_out)
);
assign Bit_Arr_out = {coreir_wrapInAsyncResetN_inst5_out,coreir_wrapInAsyncResetN_inst4_out,coreir_wrapInAsyncResetN_inst3_out,coreir_wrapInAsyncResetN_inst2_out};
assign Bit_out = coreir_wrapInAsyncResetN_inst1_out;
assign O = coreir_wrapOutAsyncResetN_inst1_out;
assign O_Arr = {coreir_wrapOutAsyncResetN_inst4_out,coreir_wrapOutAsyncResetN_inst3_out};
assign O_Tuple_B = coreir_wrapInAsyncResetN_inst0_out;
assign O_Tuple_R = coreir_wrapOutAsyncResetN_inst2_out;
endmodule

