module coreir_undriven #(
    parameter width = 1
) (
    output [width-1:0] out
);

endmodule

module Main (
    output [4:0] O_0,
    output [4:0] O_1,
    output [4:0] O_2,
    output [4:0] O_3,
    output [4:0] O_4
);
wire [4:0] undriven_inst0_out;
wire [4:0] undriven_inst1_out;
wire [4:0] undriven_inst2_out;
wire [4:0] undriven_inst3_out;
wire [4:0] undriven_inst4_out;
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
assign O_0 = undriven_inst0_out;
assign O_1 = undriven_inst1_out;
assign O_2 = undriven_inst2_out;
assign O_3 = undriven_inst3_out;
assign O_4 = undriven_inst4_out;

assign O[0] = 0;
            


assign O[1] = 1;
            


assign O[2] = 2;
            


assign O[3] = 3;
            


assign O[4] = 4;
            
endmodule

