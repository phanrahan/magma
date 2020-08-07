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
wire FF_inst0_I;
wire FF_inst0_CLK;
wire FF_inst0_CE;
wire _magma_inline_wire0;
assign FF_inst0_I = I;
assign FF_inst0_CLK = CLK;
assign FF_inst0_CE = CE;
FF FF_inst0 (
    .I(FF_inst0_I),
    .O(O),
    .CLK(FF_inst0_CLK),
    .CE(FF_inst0_CE)
);
assign _magma_inline_wire0 = O;

`ifndef MAGMA_LOG_LEVEL
    `define MAGMA_LOG_LEVEL 1
`endif

integer \_file_test_flog.log ;
initial \_file_test_flog.log = $fopen("test_flog.log", "a");

always @(posedge CLK) begin
    if ((`MAGMA_LOG_LEVEL <= 0) && (CE)) $fdisplay(\_file_test_flog.log , "[DEBUG] ff.O=%d, ff.I=%d", _magma_inline_wire0, I);
end

always @(posedge CLK) begin
    if ((`MAGMA_LOG_LEVEL <= 1) && (CE)) $fdisplay(\_file_test_flog.log , "[INFO] ff.O=%d, ff.I=%d", _magma_inline_wire0, I);
end

always @(posedge CLK) begin
    if ((`MAGMA_LOG_LEVEL <= 2) && (CE)) $fdisplay(\_file_test_flog.log , "[WARNING] ff.O=%d, ff.I=%d", _magma_inline_wire0, I);
end

always @(posedge CLK) begin
    if ((`MAGMA_LOG_LEVEL <= 3) && (CE)) $fdisplay(\_file_test_flog.log , "[ERROR] ff.O=%d, ff.I=%d", _magma_inline_wire0, I);
end


final $fclose(\_file_test_flog.log );

endmodule

