module Memory(	// <stdin>:1:1
  input  [6:0]  RADDR,
  input         CLK,
  input  [6:0]  WADDR,
  input  [11:0] WDATA,
  input         WE,
  output [11:0] RDATA);

  reg [127:0][11:0] coreir_mem128x12_inst0;	// <stdin>:2:10

  always_ff @(posedge CLK) begin	// <stdin>:6:5
    if (WE)	// <stdin>:7:9
      coreir_mem128x12_inst0[WADDR] <= WDATA;	// <stdin>:5:10, :8:13
  end // always_ff @(posedge)
  assign RDATA = coreir_mem128x12_inst0[RADDR];	// <stdin>:3:10, :4:10, :11:5
endmodule

module simple_memory_wrapper(	// <stdin>:13:1
  input  [6:0]  RADDR,
  input         CLK,
  input  [6:0]  WADDR,
  input  [11:0] WDATA,
  input         WE,
  output [11:0] RDATA);

  Memory Memory_inst0 (	// <stdin>:14:10
    .RADDR (RADDR),
    .CLK   (CLK),
    .WADDR (WADDR),
    .WDATA (WDATA),
    .WE    (WE),
    .RDATA (RDATA)
  );
endmodule

