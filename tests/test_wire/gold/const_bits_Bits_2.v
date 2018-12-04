module main (output [1:0] O);
wire [1:0] Buf_inst0_O;
Buf Buf_inst0 (.I({1'b0,1'b1}), .O(Buf_inst0_O));
assign O = Buf_inst0_O;
endmodule

