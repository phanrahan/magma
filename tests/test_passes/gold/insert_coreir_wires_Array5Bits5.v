module coreir_wire #(
    parameter width = 1
) (
    input [width-1:0] in,
    output [width-1:0] out
);
  assign out = in;
endmodule

module Main (
    input [4:0] I_0,
    input [4:0] I_1,
    input [4:0] I_2,
    input [4:0] I_3,
    input [4:0] I_4,
    output [4:0] O_0,
    output [4:0] O_1,
    output [4:0] O_2,
    output [4:0] O_3,
    output [4:0] O_4
);
wire [24:0] x_out;
coreir_wire #(
    .width(25)
) x (
    .in({I_4[4],I_4[3],I_4[2],I_4[1],I_4[0],I_3[4],I_3[3],I_3[2],I_3[1],I_3[0],I_2[4],I_2[3],I_2[2],I_2[1],I_2[0],I_1[4],I_1[3],I_1[2],I_1[1],I_1[0],I_0[4],I_0[3],I_0[2],I_0[1],I_0[0]}),
    .out(x_out)
);
assign O_0 = {x_out[4],x_out[3],x_out[2],x_out[1],x_out[0]};
assign O_1 = {x_out[9],x_out[8],x_out[7],x_out[6],x_out[5]};
assign O_2 = {x_out[14],x_out[13],x_out[12],x_out[11],x_out[10]};
assign O_3 = {x_out[19],x_out[18],x_out[17],x_out[16],x_out[15]};
assign O_4 = {x_out[24],x_out[23],x_out[22],x_out[21],x_out[20]};
endmodule

