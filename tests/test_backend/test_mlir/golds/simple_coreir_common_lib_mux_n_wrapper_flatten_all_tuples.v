// Generated by CIRCT firtool-1.48.0-34-g7018fb13b
module simple_coreir_common_lib_mux_n_wrapper(
  input  [7:0][5:0] I_data,
  input  [2:0]      I_sel,
  output [5:0]      O
);

  assign O = I_data[I_sel];
endmodule

