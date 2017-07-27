//unary ops
module coreir_not #(parameter WIDTH=16) (
  input [WIDTH-1:0] in,
  output [WIDTH-1:0] out
);
  assign out = ~in;
endmodule

module coreir_neg #(parameter WIDTH=16) (
  input [WIDTH-1:0] in,
  output [WIDTH-1:0] out
);
  assign out = -in;
endmodule

//unaryReduce ops
module coreir_xorr #(parameter WIDTH=16) (
  input [WIDTH-1:0] in,
  output out
);
  assign out = ^in;
endmodule

module coreir_orr #(parameter WIDTH=16) (
  input [WIDTH-1:0] in,
  output out
);
  assign out = |in;
endmodule

module coreir_andr #(parameter WIDTH=16) (
  input [WIDTH-1:0] in,
  output out
);
  assign out = &in;
endmodule

//binary ops
module coreir_and #(parameter WIDTH=16) (
  input [WIDTH-1:0] in0,
  input [WIDTH-1:0] in1,
  output [WIDTH-1:0] out
);
  assign out = in0 & in1;
endmodule

module coreir_dashr #(parameter WIDTH=16) (
  input [WIDTH-1:0] in0,
  input [WIDTH-1:0] in1,
  output [WIDTH-1:0] out
);
  assign out = $signed(in0) >>> in1;
endmodule

module coreir_dlshr #(parameter WIDTH=16) (
  input [WIDTH-1:0] in0,
  input [WIDTH-1:0] in1,
  output [WIDTH-1:0] out
);
  assign out = in0 >> in1;
endmodule

module coreir_xor #(parameter WIDTH=16) (
  input [WIDTH-1:0] in0,
  input [WIDTH-1:0] in1,
  output [WIDTH-1:0] out
);
  assign out = in0 ^ in1;
endmodule

module coreir_sub #(parameter WIDTH=16) (
  input [WIDTH-1:0] in0,
  input [WIDTH-1:0] in1,
  output [WIDTH-1:0] out
);
  assign out = in0 - in1;
endmodule

module coreir_sdiv #(parameter WIDTH=16) (
  input [WIDTH-1:0] in0,
  input [WIDTH-1:0] in1,
  output [WIDTH-1:0] out
);
  assign out = $signed(in0) / $signed(in1);
endmodule

module coreir_add #(parameter WIDTH=16) (
  input [WIDTH-1:0] in0,
  input [WIDTH-1:0] in1,
  output [WIDTH-1:0] out
);
  assign out = in0 + in1;
endmodule

module coreir_dshl #(parameter WIDTH=16) (
  input [WIDTH-1:0] in0,
  input [WIDTH-1:0] in1,
  output [WIDTH-1:0] out
);
  assign out = in0 << in1;
endmodule

module coreir_mul #(parameter WIDTH=16) (
  input [WIDTH-1:0] in0,
  input [WIDTH-1:0] in1,
  output [WIDTH-1:0] out
);
  assign out = in0 * in1;
endmodule

module coreir_udiv #(parameter WIDTH=16) (
  input [WIDTH-1:0] in0,
  input [WIDTH-1:0] in1,
  output [WIDTH-1:0] out
);
  assign out = in0 / in1;
endmodule

module coreir_or #(parameter WIDTH=16) (
  input [WIDTH-1:0] in0,
  input [WIDTH-1:0] in1,
  output [WIDTH-1:0] out
);
  assign out = in0 | in1;
endmodule

//static_shift ops
module coreir_lshr #(parameter WIDTH=16,parameter SHIFTBITS=1) (
  input [WIDTH-1:0] in,
  output [WIDTH-1:0] out
);
  assign out = in >> SHIFTBITS;
endmodule

module coreir_shl #(parameter WIDTH=16,parameter SHIFTBITS=1) (
  input [WIDTH-1:0] in,
  output [WIDTH-1:0] out
);
  assign out = in << SHIFTBITS;
endmodule

module coreir_ashr #(parameter WIDTH=16,parameter SHIFTBITS=1) (
  input [WIDTH-1:0] in,
  output [WIDTH-1:0] out
);
  assign out = $signed(in) >>> SHIFTBITS;
endmodule

//binaryReduce ops
module coreir_uge #(parameter WIDTH=16) (
  input [WIDTH-1:0] in0,
  input [WIDTH-1:0] in1,
  output out
);
  assign out = in0 >= in1;
endmodule

module coreir_sge #(parameter WIDTH=16) (
  input [WIDTH-1:0] in0,
  input [WIDTH-1:0] in1,
  output out
);
  assign out = $signed(in0) >= $signed(in1);
endmodule

module coreir_slt #(parameter WIDTH=16) (
  input [WIDTH-1:0] in0,
  input [WIDTH-1:0] in1,
  output out
);
  assign out = $signed(in0) < $signed(in1);
endmodule

module coreir_sle #(parameter WIDTH=16) (
  input [WIDTH-1:0] in0,
  input [WIDTH-1:0] in1,
  output out
);
  assign out = $signed(in0) <= $signed(in1);
endmodule

module coreir_ule #(parameter WIDTH=16) (
  input [WIDTH-1:0] in0,
  input [WIDTH-1:0] in1,
  output out
);
  assign out = in0 <= in1;
endmodule

module coreir_eq #(parameter WIDTH=16) (
  input [WIDTH-1:0] in0,
  input [WIDTH-1:0] in1,
  output out
);
  assign out = in0 == in1;
endmodule

module coreir_sgt #(parameter WIDTH=16) (
  input [WIDTH-1:0] in0,
  input [WIDTH-1:0] in1,
  output out
);
  assign out = $signed(in0) > $signed(in1);
endmodule

module coreir_ult #(parameter WIDTH=16) (
  input [WIDTH-1:0] in0,
  input [WIDTH-1:0] in1,
  output out
);
  assign out = in0 < in1;
endmodule

module coreir_ugt #(parameter WIDTH=16) (
  input [WIDTH-1:0] in0,
  input [WIDTH-1:0] in1,
  output out
);
  assign out = in0 > in1;
endmodule

//ternary op
module Mux #(parameter WIDTH=16) (
  input [WIDTH-1:0] d0,
  input [WIDTH-1:0] d1,
  input sel,
  output [WIDTH-1:0] out
);
  assign out = sel ? d1 : d0;
endmodule

//Now all the register permutations
module Reg_N #(parameter WIDTH=16) (
  input [WIDTH-1:0] D,
  input clk,
  output [WIDTH-1:0] Q
);
  reg [WIDTH-1:0] r;
  always @(negedge clk) begin
    r <= D;
  end
  assign Q = r;
endmodule

module Reg_P #(parameter WIDTH=16) (
  input [WIDTH-1:0] D,
  input clk,
  output [WIDTH-1:0] Q
);
  reg [WIDTH-1:0] r;
  always @(posedge clk) begin
    r <= D;
  end
  assign Q = r;
endmodule

module Reg_NR #(parameter WIDTH=16,parameter INIT=0) (
  input [WIDTH-1:0] D,
  input clk,
  input rst,
  output [WIDTH-1:0] Q
);
  reg [WIDTH-1:0] r;
  always @(negedge clk, negedge rst) begin
    if (!rst) r <= INIT;
    else r <= D;
  end
  assign Q = r;
endmodule

module Reg_PR #(parameter WIDTH=16,parameter INIT=0) (
  input [WIDTH-1:0] D,
  input clk,
  input rst,
  output [WIDTH-1:0] Q
);
  reg [WIDTH-1:0] r;
  always @(posedge clk, negedge rst) begin
    if (!rst) r <= INIT;
    else r <= D;
  end
  assign Q = r;
endmodule

module Reg_NC #(parameter WIDTH=16,parameter INIT=0) (
  input [WIDTH-1:0] D,
  input clk,
  input clr,
  output [WIDTH-1:0] Q
);
  reg [WIDTH-1:0] r;
  always @(negedge clk) begin
    r <= (clr ? INIT : D);
  end
  assign Q = r;
endmodule

module Reg_PC #(parameter WIDTH=16,parameter INIT=0) (
  input [WIDTH-1:0] D,
  input clk,
  input clr,
  output [WIDTH-1:0] Q
);
  reg [WIDTH-1:0] r;
  always @(posedge clk) begin
    r <= (clr ? INIT : D);
  end
  assign Q = r;
endmodule

module Reg_NE #(parameter WIDTH=16) (
  input [WIDTH-1:0] D,
  input clk,
  input en,
  output [WIDTH-1:0] Q
);
  reg [WIDTH-1:0] r;
  always @(negedge clk) begin
    r <= en ? D : r;
  end
  assign Q = r;
endmodule

module Reg_PE #(parameter WIDTH=16) (
  input [WIDTH-1:0] D,
  input clk,
  input en,
  output [WIDTH-1:0] Q
);
  reg [WIDTH-1:0] r;
  always @(posedge clk) begin
    r <= en ? D : r;
  end
  assign Q = r;
endmodule

module Reg_NRE #(parameter WIDTH=16,parameter INIT=0) (
  input [WIDTH-1:0] D,
  input clk,
  input en,
  input rst,
  output [WIDTH-1:0] Q
);
  reg [WIDTH-1:0] r;
  always @(negedge clk, negedge rst) begin
    if (!rst) r <= INIT;
    else r <= en ? D : r;
  end
  assign Q = r;
endmodule

module Reg_PRE #(parameter WIDTH=16,parameter INIT=0) (
  input [WIDTH-1:0] D,
  input clk,
  input en,
  input rst,
  output [WIDTH-1:0] Q
);
  reg [WIDTH-1:0] r;
  always @(posedge clk, negedge rst) begin
    if (!rst) r <= INIT;
    else r <= en ? D : r;
  end
  assign Q = r;
endmodule

module Reg_NCE #(parameter WIDTH=16,parameter INIT=0) (
  input [WIDTH-1:0] D,
  input clk,
  input clr,
  input en,
  output [WIDTH-1:0] Q
);
  reg [WIDTH-1:0] r;
  always @(negedge clk) begin
    r <= en ? (clr ? INIT : D) : r;
  end
  assign Q = r;
endmodule

module Reg_PCE #(parameter WIDTH=16,parameter INIT=0) (
  input [WIDTH-1:0] D,
  input clk,
  input clr,
  input en,
  output [WIDTH-1:0] Q
);
  reg [WIDTH-1:0] r;
  always @(posedge clk) begin
    r <= en ? (clr ? INIT : D) : r;
  end
  assign Q = r;
endmodule

