module TestBasic (
  input logic ASYNCRESET,
  input logic CLK,
  input logic [1:0] I,
  output logic [1:0] O
);

logic [1:0] _O;
logic [1:0] self_x_I;
logic [1:0] self_x_O;
logic [1:0] self_y_I;
logic [1:0] self_y_O;
always_comb begin
  _O = self_y_O;
  self_y_I = self_x_O;
  self_x_I = I;
  O = _O;
end

always_ff @(posedge CLK, posedge ASYNCRESET) begin
  if (ASYNCRESET) begin
    self_x_O <= 2'h0;
    self_y_O <= 2'h0;
  end
  else begin
    self_x_O <= self_x_I;
    self_y_O <= self_y_I;
  end
end
endmodule   // TestBasic


module TestBasic (input CLK, input [1:0] I, output [1:0] O);
wire [1:0] TestBasic_comb_inst0_O0;
wire [1:0] TestBasic_comb_inst0_O1;
wire [1:0] TestBasic_comb_inst0_O2;
wire [1:0] reg_P_inst0_out;
wire [1:0] reg_P_inst1_out;
TestBasic_comb TestBasic_comb_inst0(.I(I), .O0(TestBasic_comb_inst0_O0), .O1(TestBasic_comb_inst0_O1), .O2(TestBasic_comb_inst0_O2), .self_x_O(reg_P_inst0_out), .self_y_O(reg_P_inst1_out));
coreir_reg #(.clk_posedge(1'b1), .init(2'h0), .width(2)) reg_P_inst0(.clk(CLK), .in(TestBasic_comb_inst0_O0), .out(reg_P_inst0_out));
coreir_reg #(.clk_posedge(1'b1), .init(2'h0), .width(2)) reg_P_inst1(.clk(CLK), .in(TestBasic_comb_inst0_O1), .out(reg_P_inst1_out));
assign O = TestBasic_comb_inst0_O2;
endmodule

