//unary ops
module coreir_not #(parameter width=16) (
  input [width-1:0] in,
  output [width-1:0] out
);
  assign out = ~in;
endmodule

module coreir_neg #(parameter width=16) (
  input [width-1:0] in,
  output [width-1:0] out
);
  assign out = -in;
endmodule

//unaryReduce ops
module coreir_xorr #(parameter width=16) (
  input [width-1:0] in,
  output out
);
  assign out = ^in;
endmodule

module coreir_orr #(parameter width=16) (
  input [width-1:0] in,
  output out
);
  assign out = |in;
endmodule

module coreir_andr #(parameter width=16) (
  input [width-1:0] in,
  output out
);
  assign out = &in;
endmodule

//binary ops
module coreir_and #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output [width-1:0] out
);
  assign out = in0 & in1;
endmodule

module coreir_dashr #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output [width-1:0] out
);
  assign out = $signed(in0) >>> in1;
endmodule

module coreir_dlshr #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output [width-1:0] out
);
  assign out = in0 >> in1;
endmodule

module coreir_xor #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output [width-1:0] out
);
  assign out = in0 ^ in1;
endmodule

module coreir_sub #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output [width-1:0] out
);
  assign out = in0 - in1;
endmodule

module coreir_sdiv #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output [width-1:0] out
);
  assign out = $signed(in0) / $signed(in1);
endmodule

module coreir_add #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output [width-1:0] out
);
  assign out = in0 + in1;
endmodule

module coreir_dshl #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output [width-1:0] out
);
  assign out = in0 << in1;
endmodule

module coreir_mul #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output [width-1:0] out
);
  assign out = in0 * in1;
endmodule

module coreir_udiv #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output [width-1:0] out
);
  assign out = in0 / in1;
endmodule

module coreir_or #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output [width-1:0] out
);
  assign out = in0 | in1;
endmodule

//static_shift ops
module coreir_lshr #(parameter width=16,parameter SHIFTBITS=1) (
  input [width-1:0] in,
  output [width-1:0] out
);
  assign out = in >> SHIFTBITS;
endmodule

module coreir_shl #(parameter width=16,parameter SHIFTBITS=1) (
  input [width-1:0] in,
  output [width-1:0] out
);
  assign out = in << SHIFTBITS;
endmodule

module coreir_ashr #(parameter width=16,parameter SHIFTBITS=1) (
  input [width-1:0] in,
  output [width-1:0] out
);
  assign out = $signed(in) >>> SHIFTBITS;
endmodule

//binaryReduce ops
module coreir_uge #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output out
);
  assign out = in0 >= in1;
endmodule

module coreir_sge #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output out
);
  assign out = $signed(in0) >= $signed(in1);
endmodule

module coreir_slt #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output out
);
  assign out = $signed(in0) < $signed(in1);
endmodule

module coreir_sle #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output out
);
  assign out = $signed(in0) <= $signed(in1);
endmodule

module coreir_ule #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output out
);
  assign out = in0 <= in1;
endmodule

module coreir_eq #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output out
);
  assign out = in0 == in1;
endmodule

module coreir_sgt #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output out
);
  assign out = $signed(in0) > $signed(in1);
endmodule

module coreir_ult #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output out
);
  assign out = in0 < in1;
endmodule

module coreir_ugt #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output out
);
  assign out = in0 > in1;
endmodule

//ternary op
module coreir_mux #(parameter width=16) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  input sel,
  output [width-1:0] out
);
  assign out = sel ? in1 : in0;
endmodule

//slice op
module coreir_slice #(parameter width=16,parameter lo=0,parameter hi=16) (
  input [width-1:0] in,
  output [(hi-lo)-1:0] out
);
  assign out = in[hi-1:lo];
endmodule

//concat op
module coreir_concat #(parameter width0=16,parameter width1=16) (
  input [width0-1:0] in0,
  input [width1-1:0] in1,
  output [(width0+width1)-1:0] out
);
  assign out = {in0,in1};
endmodule

//Const op
module coreir_const #(parameter width=16,parameter value=0) (
  output [width-1:0] out
);
  assign out = value;
endmodule

//term op
module coreir_term #(parameter width=16) (
  input [width-1:0] in
);
  
endmodule

//Now all the register permutations
module coreir_reg_N #(parameter width=16,parameter init=0) (
  input [width-1:0] in,
  input clk,
  output [width-1:0] out
);
  reg [width-1:0] r;
  always @(negedge clk) begin
    r <= in;
  end
  assign out = r;
endmodule

module coreir_reg_P #(parameter width=16,parameter init=0) (
  input [width-1:0] in,
  input clk,
  output [width-1:0] out
);
  reg [width-1:0] r;
  always @(posedge clk) begin
    r <= in;
  end
  assign out = r;
endmodule

module coreir_reg_NR #(parameter width=16,parameter init=0) (
  input [width-1:0] in,
  input clk,
  input rst,
  output [width-1:0] out
);
  reg [width-1:0] r;
  always @(negedge clk, negedge rst) begin
    if (!rst) r <= init;
    else r <= in;
  end
  assign out = r;
endmodule

module coreir_reg_PR #(parameter width=16,parameter init=0) (
  input [width-1:0] in,
  input clk,
  input rst,
  output [width-1:0] out
);
  reg [width-1:0] r;
  always @(posedge clk, negedge rst) begin
    if (!rst) r <= init;
    else r <= in;
  end
  assign out = r;
endmodule

module coreir_reg_NC #(parameter width=16,parameter init=0) (
  input [width-1:0] in,
  input clk,
  input clr,
  output [width-1:0] out
);
  reg [width-1:0] r;
  always @(negedge clk) begin
    r <= (clr ? init : in);
  end
  assign out = r;
endmodule

module coreir_reg_PC #(parameter width=16,parameter init=0) (
  input [width-1:0] in,
  input clk,
  input clr,
  output [width-1:0] out
);
  reg [width-1:0] r;
  always @(posedge clk) begin
    r <= (clr ? init : in);
  end
  assign out = r;
endmodule

module coreir_reg_NE #(parameter width=16,parameter init=0) (
  input [width-1:0] in,
  input clk,
  input en,
  output [width-1:0] out
);
  reg [width-1:0] r;
  always @(negedge clk) begin
    r <= en ? in : r;
  end
  assign out = r;
endmodule

module coreir_reg_PE #(parameter width=16,parameter init=0) (
  input [width-1:0] in,
  input clk,
  input en,
  output [width-1:0] out
);
  reg [width-1:0] r;
  always @(posedge clk) begin
    r <= en ? in : r;
  end
  assign out = r;
endmodule

module coreir_reg_NRE #(parameter width=16,parameter init=0) (
  input [width-1:0] in,
  input clk,
  input en,
  input rst,
  output [width-1:0] out
);
  reg [width-1:0] r;
  always @(negedge clk, negedge rst) begin
    if (!rst) r <= init;
    else r <= en ? in : r;
  end
  assign out = r;
endmodule

module coreir_reg_PRE #(parameter width=16,parameter init=0) (
  input [width-1:0] in,
  input clk,
  input en,
  input rst,
  output [width-1:0] out
);
  reg [width-1:0] r;
  always @(posedge clk, negedge rst) begin
    if (!rst) r <= init;
    else r <= en ? in : r;
  end
  assign out = r;
endmodule

module coreir_reg_NCE #(parameter width=16,parameter init=0) (
  input [width-1:0] in,
  input clk,
  input clr,
  input en,
  output [width-1:0] out
);
  reg [width-1:0] r;
  always @(negedge clk) begin
    r <= en ? (clr ? init : in) : r;
  end
  assign out = r;
endmodule

module coreir_reg_PCE #(parameter width=16,parameter init=0) (
  input [width-1:0] in,
  input clk,
  input clr,
  input en,
  output [width-1:0] out
);
  reg [width-1:0] r;
  always @(posedge clk) begin
    r <= en ? (clr ? init : in) : r;
  end
  assign out = r;
endmodule

module coreir_mem #(parameter width=16,parameter depth=1024) (
  input [$clog2(depth)-1:0] raddr,
  input [$clog2(depth)-1:0] waddr,
  input [width-1:0] wdata,
  input rclk,
  input ren,
  input wclk,
  input wen,
  output [width-1:0] rdata
);

reg [width-1:0] data[depth-1:0];
reg [width-1:0] outreg;

always @(posedge wclk) begin
  if (wen) begin
    data[waddr] <= wdata;
  end
end

always @(posedge rclk) begin
  if (ren) begin
    outreg <= data[raddr];
  end
end

assign rdata = outreg;
//Initialize to X
integer i;
initial begin
  outreg = {width{1'bx}};
  for (i=0; i<depth; i+=1) begin
    data[i] = {width{1'bx}};
  end
end

endmodule

