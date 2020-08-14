module FF(input clk, input rst, input d, output q);

parameter init = 0;

reg ff; 
always @(posedge clk or posedge rst) begin
  if (!rst)
    ff <= init;
  else
    ff <= d; 
end

assign q = ff;
endmodule
module Top (
    input [1:0] I,
    output [1:0] O,
    input CLK,
    input ASYNCRESET
);
wire FF_inst0_q;
wire FF_inst1_q;
FF #(
    .init(0)
) FF_inst0 (
    .clk(CLK),
    .rst(ASYNCRESET),
    .d(I[0]),
    .q(FF_inst0_q)
);
FF #(
    .init(1)
) FF_inst1 (
    .clk(CLK),
    .rst(ASYNCRESET),
    .d(I[1]),
    .q(FF_inst1_q)
);
assign O = {FF_inst1_q,FF_inst0_q};
endmodule

