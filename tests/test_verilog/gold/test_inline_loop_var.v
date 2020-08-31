module coreir_undriven #(
    parameter width = 1
) (
    output [width-1:0] out
);

endmodule

module corebit_term (
    input in
);

endmodule

module corebit_const #(
    parameter value = 1
) (
    output out
);
  assign out = value;
endmodule

module Main (
    output [4:0] O [4:0]
);
wire bit_const_0_None_out;
wire [4:0] undriven_inst0_out;
wire [4:0] undriven_inst1_out;
wire [4:0] undriven_inst2_out;
wire [4:0] undriven_inst3_out;
wire [4:0] undriven_inst4_out;
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
coreir_undriven #(
    .width(5)
) undriven_inst0 (
    .out(undriven_inst0_out)
);
coreir_undriven #(
    .width(5)
) undriven_inst1 (
    .out(undriven_inst1_out)
);
coreir_undriven #(
    .width(5)
) undriven_inst2 (
    .out(undriven_inst2_out)
);
coreir_undriven #(
    .width(5)
) undriven_inst3 (
    .out(undriven_inst3_out)
);
coreir_undriven #(
    .width(5)
) undriven_inst4 (
    .out(undriven_inst4_out)
);
assign O[4] = undriven_inst4_out;
assign O[3] = undriven_inst3_out;
assign O[2] = undriven_inst2_out;
assign O[1] = undriven_inst1_out;
assign O[0] = undriven_inst0_out;

assign O[0] = 0;
            

assign O[1] = 1;
            

assign O[2] = 2;
            

assign O[3] = 3;
            

assign O[4] = 4;
            
endmodule

