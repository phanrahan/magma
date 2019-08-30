module sram_512w_16b (Q, CLK, CEN, WEN, A, D, EMA, EMAW, EMAS, TEN, BEN, RET1N, STOV);
   output reg [15:0] Q;
   input        CLK;
   input        CEN;
   input        WEN;
   input [8:0]  A;
   input [15:0] D;
   
   input [2:0]  EMA;
   input [1:0]  EMAW;
   input        EMAS;
   input        TEN;
   input        BEN;
   input        RET1N;
   input        STOV;
   
   reg [15:0]   data_array [0:511];

   always @(posedge CLK) begin

      // Use all the unused wires (note at least one of them must be nonzero!)
      if (| {EMA, EMAW, EMAS, TEN, BEN, RET1N, STOV}) begin
         if (CEN == 1'b0) begin                  // ACTIVE LOW!!
            Q = data_array[A];
            if (WEN == 1'b0) data_array[A] = D;  // ACTIVE LOW!!
         end
      end
   end
endmodule
module coreir_const #(parameter width = 1, parameter value = 1) (output [width-1:0] out);
  assign out = value;
endmodule

module corebit_not (input in, output out);
  assign out = ~in;
endmodule

module corebit_const #(parameter value = 1) (output out);
  assign out = value;
endmodule

module Mem (input [8:0] addr, input cen, input clk, input [15:0] data_in, output [15:0] data_out, input wen);
wire bit_const_0_None_out;
wire bit_const_1_None_out;
wire [1:0] const_0_2_out;
wire [2:0] const_0_3_out;
wire [15:0] mem_inst_Q;
wire not_inst0_out;
wire not_inst1_out;
corebit_const #(.value(0)) bit_const_0_None(.out(bit_const_0_None_out));
corebit_const #(.value(1)) bit_const_1_None(.out(bit_const_1_None_out));
coreir_const #(.value(2'h0), .width(2)) const_0_2(.out(const_0_2_out));
coreir_const #(.value(3'h0), .width(3)) const_0_3(.out(const_0_3_out));
sram_512w_16b mem_inst(.A(addr), .BEN(bit_const_1_None_out), .CEN(not_inst0_out), .CLK(clk), .D(data_in), .EMA(const_0_3_out), .EMAS(bit_const_0_None_out), .EMAW(const_0_2_out), .Q(mem_inst_Q), .RET1N(bit_const_1_None_out), .STOV(bit_const_0_None_out), .TEN(bit_const_1_None_out), .WEN(not_inst1_out));
corebit_not not_inst0(.in(cen), .out(not_inst0_out));
corebit_not not_inst1(.in(wen), .out(not_inst1_out));
assign data_out = mem_inst_Q;
endmodule

