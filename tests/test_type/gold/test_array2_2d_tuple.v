module coreir_wire #(
    parameter width = 1
) (
    input [width-1:0] in,
    output [width-1:0] out
);
  assign out = in;
endmodule

module Foo (
    input [3:0] I_c_0_a [3:0],
    input [3:0] I_c_1_a [3:0],
    output [3:0] O_c_0_a [3:0],
    output [3:0] O_c_1_a [3:0]
);
wire [31:0] temp_out;
wire [31:0] temp_in;
assign temp_in = {I_c_0_a[0],I_c_0_a[1],I_c_0_a[2],I_c_0_a[3],I_c_1_a[0],I_c_1_a[1],I_c_1_a[2],I_c_1_a[3]};
coreir_wire #(
    .width(32)
) temp (
    .in(temp_in),
    .out(temp_out)
);
assign O_c_0_a[3] = {temp_out[15],temp_out[14],temp_out[13],temp_out[12]};
assign O_c_0_a[2] = {temp_out[11],temp_out[10],temp_out[9],temp_out[8]};
assign O_c_0_a[1] = {temp_out[7],temp_out[6],temp_out[5],temp_out[4]};
assign O_c_0_a[0] = {temp_out[3],temp_out[2],temp_out[1],temp_out[0]};
assign O_c_1_a[3] = {temp_out[31],temp_out[30],temp_out[29],temp_out[28]};
assign O_c_1_a[2] = {temp_out[27],temp_out[26],temp_out[25],temp_out[24]};
assign O_c_1_a[1] = {temp_out[23],temp_out[22],temp_out[21],temp_out[20]};
assign O_c_1_a[0] = {temp_out[19],temp_out[18],temp_out[17],temp_out[16]};
endmodule

