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
wire FF_inst0_clk;
wire FF_inst0_rst;
wire FF_inst0_d;
wire FF_inst0_q;
wire FF_inst1_clk;
wire FF_inst1_rst;
wire FF_inst1_d;
wire FF_inst1_q;
assign FF_inst0_clk = CLK;
assign FF_inst0_rst = ASYNCRESET;
assign FF_inst0_d = I[0];
FF #(
    .init(0)
) FF_inst0 (
    .clk(FF_inst0_clk),
    .rst(FF_inst0_rst),
    .d(FF_inst0_d),
    .q(FF_inst0_q)
);
assign FF_inst1_clk = CLK;
assign FF_inst1_rst = ASYNCRESET;
assign FF_inst1_d = I[1];
FF #(
    .init(1)
) FF_inst1 (
    .clk(FF_inst1_clk),
    .rst(FF_inst1_rst),
    .d(FF_inst1_d),
    .q(FF_inst1_q)
);
assign O = {FF_inst1_q,FF_inst0_q};
endmodule

