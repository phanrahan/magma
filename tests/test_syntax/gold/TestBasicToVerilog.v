module TestBasic (
  input logic ASYNCRESET,
  input logic CLK,
  input logic [1:0] I,
  output logic [1:0] O
);

logic [1:0] x;
logic [1:0] y;

always_ff @(posedge CLK, posedge ASYNCRESET) begin
  if (ASYNCRESET) begin
    x <= 2'h0;
    y <= 2'h0;
  end
  else begin
    y <= x;
    x <= I;
    O <= y;
  end
end
endmodule   // TestBasic


