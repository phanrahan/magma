module main (input  I, output  O);
wire  Buf_inst0_O;
wire  Buf_inst1_O;
Buf Buf_inst0 (.I(I), .O(Buf_inst0_O));
Buf Buf_inst1 (.I(Buf_inst0_O), .O(Buf_inst1_O));
assign O = Buf_inst1_O;
endmodule

