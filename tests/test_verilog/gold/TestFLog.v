module coreir_wrap (
    input in,
    output out
);
  assign out = in;
endmodule

module corebit_term (
    input in
);

endmodule

module FF(input I, output reg O, input CLK, input CE);
always @(posedge CLK) begin
  if (CE) O <= I;
end
endmodule
module TestFLog (
    input I,
    output O,
    input CLK,
    input CE
);
wire FF_inst0_O;
wire coreir_wrapInClock_inst0_out;
FF FF_inst0 (
    .I(I),
    .O(FF_inst0_O),
    .CLK(CLK),
    .CE(CE)
);
corebit_term corebit_term_inst0 (
    .in(coreir_wrapInClock_inst0_out)
);
corebit_term corebit_term_inst1 (
    .in(CE)
);
coreir_wrap coreir_wrapInClock_inst0 (
    .in(CLK),
    .out(coreir_wrapInClock_inst0_out)
);
assign O = FF_inst0_O;

`ifndef MAGMA_LOG_LEVEL
    `define MAGMA_LOG_LEVEL 1
`endif


integer \_file_test_flog.log ;
initial \_file_test_flog.log = $fopen("test_flog.log", "a");


always @(posedge CLK) begin
    if ((`MAGMA_LOG_LEVEL <= 0) && (CE)) $fdisplay(\_file_test_flog.log , "[DEBUG] ff.O=%d, ff.I=%d", FF_inst0.O, FF_inst0.I);
end


always @(posedge CLK) begin
    if ((`MAGMA_LOG_LEVEL <= 1) && (CE)) $fdisplay(\_file_test_flog.log , "[INFO] ff.O=%d, ff.I=%d", FF_inst0.O, FF_inst0.I);
end


always @(posedge CLK) begin
    if ((`MAGMA_LOG_LEVEL <= 2) && (CE)) $fdisplay(\_file_test_flog.log , "[WARNING] ff.O=%d, ff.I=%d", FF_inst0.O, FF_inst0.I);
end


always @(posedge CLK) begin
    if ((`MAGMA_LOG_LEVEL <= 3) && (CE)) $fdisplay(\_file_test_flog.log , "[ERROR] ff.O=%d, ff.I=%d", FF_inst0.O, FF_inst0.I);
end



final $fclose(\_file_test_flog.log );

endmodule

