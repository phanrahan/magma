module main (input  I, output  O);
wire  buf1_O;
wire  buf2_O;
Buf buf1 (.I(I), .O(buf1_O));
Buf buf2 (.I(buf1_O), .O(buf2_O));
assign O = buf2_O;
endmodule

