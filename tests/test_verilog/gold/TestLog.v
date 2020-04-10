module corebit_term (
    input in
);

endmodule

module FF(input I, output reg O, input CLK, input CE);
always @(posedge CLK) begin
  if (CE) O <= I;
end
endmodule
module TestLog (
    input I,
    output O,
    input CLK,
    input CE
);
wire O_magma_inline_wire;
FF FF_inst0 (
    .I(I),
    .O(O),
    .CLK(CLK),
    .CE(CE)
);
assign O_magma_inline_wire = O;
corebit_term corebit_term_inst0 (
    .in(O_magma_inline_wire)
);

`ifndef MAGMA_LOG_LEVEL
    `define MAGMA_LOG_LEVEL 1
`endif

always @(posedge CLK) begin
    if ((`MAGMA_LOG_LEVEL <= 0) && (CE)) $display("[DEBUG] ff.O=%d, ff.I=%d", O_magma_inline_wire, I);
end


always @(posedge CLK) begin
    if ((`MAGMA_LOG_LEVEL <= 1) && (CE)) $display("[INFO] ff.O=%d, ff.I=%d", O_magma_inline_wire, I);
end


always @(posedge CLK) begin
    if ((`MAGMA_LOG_LEVEL <= 2) && (CE)) $display("[WARNING] ff.O=%d, ff.I=%d", O_magma_inline_wire, I);
end


always @(posedge CLK) begin
    if ((`MAGMA_LOG_LEVEL <= 3) && (CE)) $display("[ERROR] ff.O=%d, ff.I=%d", O_magma_inline_wire, I);
end

endmodule

