module main (input  I, output  O);
wire  buf_O;
Buf buf (.I(I), .O(buf_O));
assign O = buf_O;
endmodule

