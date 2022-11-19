module main (output  O);
wire  buf_O;
Buf buf (.I(1'b1), .O(buf_O));
assign O = buf_O;
endmodule

