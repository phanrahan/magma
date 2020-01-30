module orr_4 (input [3:0] I, output O);
    assign O = |(I);
endmodule
module logical_and (input I0, input I1, output O);
    assign O = I0 && I1;
endmodule
module andr_4 (input [3:0] I, output O);
    assign O = &(I);
endmodule
module RTL (input CLK, input handshake_arr_0_ready, output handshake_arr_0_valid, input handshake_arr_1_ready, output handshake_arr_1_valid, input handshake_arr_2_ready, output handshake_arr_2_valid, input handshake_ready, output handshake_valid, input [3:0] in1, input [3:0] in2, output out);
wire andr_4_inst0_O;
wire logical_and_inst0_O;
wire orr_4_inst0_O;
andr_4 andr_4_inst0(.I(in1), .O(andr_4_inst0_O));
logical_and logical_and_inst0(.I0(orr_4_inst0_O), .I1(andr_4_inst0_O), .O(logical_and_inst0_O));
orr_4 orr_4_inst0(.I(in1), .O(orr_4_inst0_O));
assign handshake_arr_0_valid = handshake_arr_2_ready;
assign handshake_arr_1_valid = handshake_arr_1_ready;
assign handshake_arr_2_valid = handshake_arr_0_ready;
assign handshake_valid = handshake_ready;
assign out = logical_and_inst0_O;
endmodule

