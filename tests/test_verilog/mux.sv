module onehot_mux_hier ( 
	input logic  [0 : 0] I0, 
	input logic  [0 : 0] I1, 
	input logic  [0 : 0] I2, 
	input logic  [0 : 0] I3, 
	input logic  [0 : 0] I4, 
	input logic  [0 : 0] I5, 
	input logic  [0 : 0] I6, 
	input logic  [0 : 0] I7, 
	input logic  [2 : 0] S ,
	output logic [0 : 0] O); 
	
logic  [7 : 0] out_sel;

precoder u_precoder ( 
	.S(S), 
	.out_sel(out_sel)); 

mux_logic u_mux_logic ( 
	.I0 (I0),
	.I1 (I1),
	.I2 (I2),
	.I3 (I3),
	.I4 (I4),
	.I5 (I5),
	.I6 (I6),
	.I7 (I7),
	.out_sel(out_sel), 
	.O(O)); 

endmodule 

module precoder ( 
	input logic  [2 : 0] S ,
	output logic  [7 : 0] out_sel );

always_comb begin: mux_sel 
	case (S) 
		3'h0    :   out_sel = 8'b00000001; 
		3'h1    :   out_sel = 8'b00000010; 
		3'h2    :   out_sel = 8'b00000100; 
		3'h3    :   out_sel = 8'b00001000; 
		3'h4    :   out_sel = 8'b00010000; 
		3'h5    :   out_sel = 8'b00100000; 
		3'h6    :   out_sel = 8'b01000000; 
		3'h7    :   out_sel = 8'b10000000; 
		default :   out_sel = 8'b0; 
	endcase 
end 

endmodule 

module mux_logic ( 
	input logic  [7 : 0] out_sel,
	input logic  [0 : 0] I0, 
	input logic  [0 : 0] I1, 
	input logic  [0 : 0] I2, 
	input logic  [0 : 0] I3, 
	input logic  [0 : 0] I4, 
	input logic  [0 : 0] I5, 
	input logic  [0 : 0] I6, 
	input logic  [0 : 0] I7, 
	output logic [0 : 0] O); 

always_comb begin: out_sel_logic 
	case (out_sel) 
		8'b00000001    :   O = I0; 
		8'b00000010    :   O = I1; 
		8'b00000100    :   O = I2; 
		8'b00001000    :   O = I3; 
		8'b00010000    :   O = I4; 
		8'b00100000    :   O = I5; 
		8'b01000000    :   O = I6; 
		8'b10000000    :   O = I7; 
		default :   O = I0; 
	endcase 
end 
endmodule 
