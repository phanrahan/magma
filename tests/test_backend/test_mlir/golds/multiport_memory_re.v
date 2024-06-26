module multiport_memory_re(
  input  [1:0] raddr_0,
               raddr_1,
               waddr_0,
  input  [4:0] wdata_0,
  input        we_0,
  input  [1:0] waddr_1,
  input  [4:0] wdata_1,
  input        we_1,
               clk,
               re_0,
               re_1,
  output [4:0] rdata_0,
               rdata_1
);

  reg [3:0][4:0] MultiportMemory_inst0;
  reg [4:0]      read_reg_0;
  reg [4:0]      read_reg_1;
  always_ff @(posedge clk) begin
    if (we_0)
      MultiportMemory_inst0[waddr_0] <= wdata_0;
    if (we_1)
      MultiportMemory_inst0[waddr_1] <= wdata_1;
    if (re_0)
      read_reg_0 <= MultiportMemory_inst0[raddr_0];
    if (re_1)
      read_reg_1 <= MultiportMemory_inst0[raddr_1];
  end // always_ff @(posedge)
  assign rdata_0 = read_reg_0;
  assign rdata_1 = read_reg_1;
endmodule

