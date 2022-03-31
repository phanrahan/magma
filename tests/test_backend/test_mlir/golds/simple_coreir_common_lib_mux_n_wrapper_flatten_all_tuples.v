module simple_coreir_common_lib_mux_n_wrapper(	// <stdin>:1:1
  input  [7:0][5:0] I_data,
  input  [2:0]      I_sel,
  output [5:0]      O);

  assign O = I_data[I_sel];	// <stdin>:2:10, :3:5
endmodule

