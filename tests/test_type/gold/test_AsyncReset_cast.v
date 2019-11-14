module coreir_wrap (input in, output out);
  assign out = in;
endmodule

module AsyncResetTest (input I, output O);
wire coreir_wrapAsyncReset_inst0_out;
coreir_wrap coreir_wrapAsyncReset_inst0(.in(I), .out(coreir_wrapAsyncReset_inst0_out));
assign O = coreir_wrapAsyncReset_inst0_out;
endmodule

