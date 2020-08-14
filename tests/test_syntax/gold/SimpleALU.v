module execute_alu (
  input logic [15:0] a,
  input logic [15:0] b,
  input logic [1:0] config_,
  output logic [15:0] O
);

logic [15:0] c;
always_comb begin
  unique case (config_)
    2'h0: c = a + b;
    2'h1: c = a - b;
    2'h2: c = a * b;
    default: c = 16'h0;
  endcase
  O = c;
end
endmodule   // execute_alu


module SimpleALU (
    input [15:0] a,
    input [15:0] b,
    output [15:0] c,
    input [1:0] config_
);
wire [15:0] execute_alu_inst0_O;
execute_alu execute_alu_inst0 (
    .a(a),
    .b(b),
    .config_(config_),
    .O(execute_alu_inst0_O)
);
assign c = execute_alu_inst0_O;
endmodule

