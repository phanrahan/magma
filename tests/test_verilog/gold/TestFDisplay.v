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

integer \_file_test_fdisplay.log ;
initial \_file_test_fdisplay.log = $fopen("test_fdisplay.log", "a");


always @(posedge CLK) begin
    if (CE) $fdisplay(\_file_test_fdisplay.log , "ff.O=%d, ff.I=%d", O_magma_inline_wire, I);
end



final $fclose(\_file_test_fdisplay.log );

endmodule

