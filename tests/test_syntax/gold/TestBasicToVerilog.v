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

always_ff @(posedge CLK, posedge ASYNCRESET) begin
  self_x_O <= self_x_I;
  self_y_O <= self_y_I;
end
always_comb begin
  _O = self_y_O;
  self_y_I = self_x_O;
  self_x_I = I;
  O = _O;
end
endmodule   // TestBasic


