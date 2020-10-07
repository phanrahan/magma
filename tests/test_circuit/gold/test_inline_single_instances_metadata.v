module mux_aoi_2_16 (
    input logic  [15 : 0] I0,
    input logic  [15 : 0] I1,
    input logic S,
    output logic [15 : 0] O);

    logic  [1 : 0] out_sel;
    logic  [15 : 0] O_int0;

precoder_16_2 u_precoder (
    .S(S),
    .out_sel(out_sel));

mux_logic_16_2 u_mux_logic (
    .I0 (I0),
    .I1 (I1),
    .out_sel(out_sel),
    .O0(O_int0));
    assign O = (  	O_int0 	);

endmodule
module MuxWrapperAOIImpl_2_16 (
    input [15:0] I [1:0],
    output [15:0] O,
    input [0:0] S
);
wire [15:0] mux_aoi_2_16_inst0_O;
mux_aoi_2_16 mux_aoi_2_16_inst0 (
    .I0(I[0]),
    .I1(I[1]),
    .S(S[0]),
    .O(mux_aoi_2_16_inst0_O)
);
assign O = mux_aoi_2_16_inst0_O;
endmodule

module Top (
    input [15:0] I [1:0],
    output [15:0] O,
    input [0:0] S
);
wire [15:0] MuxWrapperAOIImpl_2_16_inst0_O;
wire [15:0] MuxWrapperAOIImpl_2_16_inst0_I [1:0];
assign MuxWrapperAOIImpl_2_16_inst0_I[1] = I[1];
assign MuxWrapperAOIImpl_2_16_inst0_I[0] = I[0];
MuxWrapperAOIImpl_2_16 MuxWrapperAOIImpl_2_16_inst0 (
    .I(MuxWrapperAOIImpl_2_16_inst0_I),
    .O(MuxWrapperAOIImpl_2_16_inst0_O),
    .S(S)
);
assign O = MuxWrapperAOIImpl_2_16_inst0_O;
endmodule

