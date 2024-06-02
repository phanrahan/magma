module Memory(
  input  [1:0]                                                                        RADDR,
  input                                                                               CLK,
  input  [1:0]                                                                        WADDR,
  input  struct packed {logic sign; logic [7:0] exponent; logic [22:0] significand; } WDATA,
  input                                                                               WE,
  output struct packed {logic sign; logic [7:0] exponent; logic [22:0] significand; } RDATA
);

  reg [3:0][31:0] coreir_mem4x32_inst0;
  always_ff @(posedge CLK) begin
    if (WE)
      coreir_mem4x32_inst0[WADDR] <= {WDATA.significand, WDATA.exponent, WDATA.sign};
  end // always_ff @(posedge)
  assign RDATA =
    '{sign: (coreir_mem4x32_inst0[RADDR][0]),
      exponent: (coreir_mem4x32_inst0[RADDR][8:1]),
      significand: (coreir_mem4x32_inst0[RADDR][31:9])};
endmodule

module FIFO(
  input                                                                               data_in_valid,
  input  struct packed {logic sign; logic [7:0] exponent; logic [22:0] significand; } data_in_data,
  input                                                                               data_out_ready,
                                                                                      CLK,
  output                                                                              data_in_ready,
                                                                                      data_out_valid,
  output struct packed {logic sign; logic [7:0] exponent; logic [22:0] significand; } data_out_data
);

  wire       _GEN;
  reg  [2:0] Register_inst0;
  wire       _GEN_0 = data_in_valid & ~_GEN;
  reg  [2:0] Register_inst1;
  always_ff @(posedge CLK) begin
    automatic logic [1:0][2:0] _GEN_1;
    automatic logic [1:0][2:0] _GEN_2;
    _GEN_1 = {{Register_inst0 + 3'h1}, {Register_inst0}};
    Register_inst0 <= _GEN_1[data_out_ready];
    _GEN_2 = {{Register_inst1 + 3'h1}, {Register_inst1}};
    Register_inst1 <= _GEN_2[_GEN_0];
  end // always_ff @(posedge)
  initial begin
    Register_inst0 = 3'h0;
    Register_inst1 = 3'h0;
  end // initial
  assign _GEN =
    Register_inst0[1:0] == Register_inst1[1:0] & (Register_inst0[2] ^ Register_inst1[2]);
  Memory Memory_inst0 (
    .RADDR (Register_inst0[1:0]),
    .CLK   (CLK),
    .WADDR (Register_inst1[1:0]),
    .WDATA (data_in_data),
    .WE    (_GEN_0),
    .RDATA (data_out_data)
  );
  assign data_in_ready = ~_GEN;
  assign data_out_valid = data_out_ready;
endmodule

