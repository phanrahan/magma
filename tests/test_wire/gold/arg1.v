module main (input  I, output  O);
wire  Buf_inst0_O;
Buf Buf_inst0 (.I(I), .O(Buf_inst0_O));
assign O = Buf_inst0_O;
endmodule

