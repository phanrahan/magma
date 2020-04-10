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
module TestDisplay (
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
    .in(FF_inst0_O)
);
corebit_term corebit_term_inst1 (
    .in(coreir_wrapInClock_inst0_out)
);
corebit_term corebit_term_inst2 (
    .in(CE)
);
coreir_wrap coreir_wrapInClock_inst0 (
    .in(CLK),
    .out(coreir_wrapInClock_inst0_out)
);
assign O = FF_inst0_O;
always @(posedge CLK) begin
    if (CE) $display("%0t: ff.O=%d, ff.I=%d", $time, FF_inst0.O, FF_inst0.I);
end

endmodule

