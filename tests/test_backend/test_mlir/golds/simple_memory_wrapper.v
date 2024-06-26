module Memory(
  input  [6:0]  RADDR,
  input         CLK,
  input  [6:0]  WADDR,
  input  [11:0] WDATA,
  input         WE,
  output [11:0] RDATA
);

  reg [127:0][11:0] coreir_mem128x12_inst0;
  always_ff @(posedge CLK) begin
    if (WE)
      coreir_mem128x12_inst0[WADDR] <= WDATA;
  end // always_ff @(posedge)
  assign RDATA = coreir_mem128x12_inst0[RADDR];
endmodule

module simple_memory_wrapper(
  input  [6:0]  RADDR,
  input         CLK,
  input  [6:0]  WADDR,
  input  [11:0] WDATA,
  input         WE,
  output [11:0] RDATA
);

  Memory Memory_inst0 (
    .RADDR (RADDR),
    .CLK   (CLK),
    .WADDR (WADDR),
    .WDATA (WDATA),
    .WE    (WE),
    .RDATA (RDATA)
  );
endmodule

