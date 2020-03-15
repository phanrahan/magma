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
module TestFDisplay (
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

integer \_file_test_fdisplay.log ;
initial \_file_test_fdisplay.log = $fopen("test_fdisplay.log", "a");


always @(posedge CLK) begin
    if (CE) $fdisplay(\_file_test_fdisplay.log , "ff.O=%d, ff.I=%d", FF_inst0.O, FF_inst0.I);
end



final $fclose(\_file_test_fdisplay.log );

endmodule

