module corebit_term (
    input in
);

endmodule

module FF(input I, output reg O, input CLK, input CE);
always @(posedge CLK) begin
  if (CE) O <= I;
end
endmodule
module TestFDisplay (
    input I,
    output O,
    input CLK,
    input CE
);
wire _magma_inline_wire0;
FF FF_inst0 (
    .I(I),
    .O(O),
    .CLK(CLK),
    .CE(CE)
);
assign _magma_inline_wire0 = O;
corebit_term corebit_term_inst0 (
    .in(_magma_inline_wire0)
);

integer \_file_test_fdisplay.log ;
initial \_file_test_fdisplay.log = $fopen("test_fdisplay.log", "a");


always @(posedge CLK) begin
    if (CE) $fdisplay(\_file_test_fdisplay.log , "ff.O=%d, ff.I=%d", _magma_inline_wire0, I);
end



final $fclose(\_file_test_fdisplay.log );

endmodule

