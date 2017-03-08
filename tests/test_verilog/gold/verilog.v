module Add (input  A, input  B, output  C);
C = A ^ B;
endmodule

module main (input  I0, input  I1, output  O);
wire  inst0_C;
Add inst0 (.A(I0), .B(I1), .C(inst0_C));
assign O = inst0_C;
endmodule

