module Counter(
  input         CLK,
  output [20:0] O,
  output        COUT
);

  reg [20:0] Register_inst0;
  always_ff @(posedge CLK) begin
    automatic logic [1:0][20:0] _GEN;
    _GEN = {{21'h0}, {Register_inst0 + 21'h1}};
    Register_inst0 <= _GEN[Register_inst0 == 21'h124F7F];
  end // always_ff @(posedge)
  initial
    Register_inst0 = 21'h0;
  assign O = Register_inst0;
  assign COUT = Register_inst0 == 21'h124F7F;
endmodule

module bcd8_increment(
  input  [7:0] din,
  output [7:0] dout
);

  reg [7:0] _GEN;
  always_comb begin
    if (din == 8'h63)
      _GEN = {1'h0, 1'h0, 1'h0, 1'h0, 1'h0, 1'h0, 1'h0, 1'h0};
    else if (din[3:0] == 4'h9) begin
      automatic logic [3:0] _GEN_0 = din[7:4] + 4'h1;
      _GEN = {1'h0, 1'h0, 1'h0, 1'h0, _GEN_0[3], _GEN_0[2], _GEN_0[1], _GEN_0[0]};
    end
    else begin
      automatic logic [3:0] _GEN_1 = din[3:0] + 4'h1;
      _GEN = {_GEN_1[3], _GEN_1[2], _GEN_1[1], _GEN_1[0], din[7], din[6], din[5], din[4]};
    end
  end // always_comb
  assign dout = _GEN;
endmodule

module seven_seg_hex(
  input  [3:0] din,
  output [6:0] dout
);

  wire [1:0][6:0] _GEN = '{7'h3F, 7'h40};
  wire [1:0][6:0] _GEN_0 = {{7'h6}, {_GEN[din == 4'h0]}};
  wire [1:0][6:0] _GEN_1 = {{7'h5B}, {_GEN_0[din == 4'h1]}};
  wire [1:0][6:0] _GEN_2 = {{7'h4F}, {_GEN_1[din == 4'h2]}};
  wire [1:0][6:0] _GEN_3 = {{7'h66}, {_GEN_2[din == 4'h3]}};
  wire [1:0][6:0] _GEN_4 = {{7'h6D}, {_GEN_3[din == 4'h4]}};
  wire [1:0][6:0] _GEN_5 = {{7'h7D}, {_GEN_4[din == 4'h5]}};
  wire [1:0][6:0] _GEN_6 = {{7'h7}, {_GEN_5[din == 4'h6]}};
  wire [1:0][6:0] _GEN_7 = {{7'h7F}, {_GEN_6[din == 4'h7]}};
  wire [1:0][6:0] _GEN_8 = {{7'h6F}, {_GEN_7[din == 4'h8]}};
  wire [1:0][6:0] _GEN_9 = {{7'h77}, {_GEN_8[din == 4'h9]}};
  wire [1:0][6:0] _GEN_10 = {{7'h7C}, {_GEN_9[din == 4'hA]}};
  wire [1:0][6:0] _GEN_11 = {{7'h39}, {_GEN_10[din == 4'hB]}};
  wire [1:0][6:0] _GEN_12 = {{7'h5E}, {_GEN_11[din == 4'hC]}};
  wire [1:0][6:0] _GEN_13 = {{7'h79}, {_GEN_12[din == 4'hD]}};
  wire [1:0][6:0] _GEN_14 = {{7'h71}, {_GEN_13[din == 4'hE]}};
  assign dout = _GEN_14[&din];
endmodule

module Counter_unq1(
  input        CLK,
  output [9:0] O
);

  reg [9:0] Register_inst0;
  always_ff @(posedge CLK)
    Register_inst0 <= Register_inst0 + 10'h1;
  initial
    Register_inst0 = 10'h0;
  assign O = Register_inst0;
endmodule

module seven_seg_ctrl(
  input        CLK,
  input  [7:0] din,
  output [7:0] dout
);

  reg  [7:0] Register_inst0;
  wire [6:0] _seven_seg_hex_inst1_dout;
  wire [6:0] _seven_seg_hex_inst0_dout;
  wire [9:0] _Counter_inst0_O;
  reg        Register_inst1;
  reg        Register_inst2;
  reg  [6:0] _GEN;
  reg        _GEN_0;
  always_comb begin
    _GEN = Register_inst0[6:0];
    _GEN_0 = Register_inst0[7];
    if (Register_inst1) begin
      if (Register_inst2) begin
        _GEN = ~_seven_seg_hex_inst0_dout;
        _GEN_0 = 1'h0;
      end
      else begin
        _GEN = ~_seven_seg_hex_inst1_dout;
        _GEN_0 = 1'h1;
      end
    end
  end // always_comb
  always_ff @(posedge CLK) begin
    Register_inst1 <= &_Counter_inst0_O;
    Register_inst2 <= Register_inst2 ^ Register_inst1;
    Register_inst0 <= {_GEN_0, _GEN};
  end // always_ff @(posedge)
  initial begin
    Register_inst1 = 1'h0;
    Register_inst2 = 1'h0;
    Register_inst0 = 8'h0;
  end // initial
  Counter_unq1 Counter_inst0 (
    .CLK (CLK),
    .O   (_Counter_inst0_O)
  );
  seven_seg_hex seven_seg_hex_inst0 (
    .din  (din[7:4]),
    .dout (_seven_seg_hex_inst0_dout)
  );
  seven_seg_hex seven_seg_hex_inst1 (
    .din  (din[3:0]),
    .dout (_seven_seg_hex_inst1_dout)
  );
  assign dout = Register_inst0;
endmodule

module top(
  input  CLK,
         BTN_N,
         BTN1,
         BTN2,
         BTN3,
  output LED1,
         LED2,
         LED3,
         LED4,
         LED5,
         P1A1,
         P1A2,
         P1A3,
         P1A4,
         P1A7,
         P1A8,
         P1A9,
         P1A10
);

  reg  [7:0]      Register_inst0;
  reg  [4:0]      _GEN;
  reg             _GEN_0;
  wire [7:0]      _seven_seg_ctrl_inst0_dout;
  wire [7:0]      _bcd8_increment_inst0_dout;
  wire            _Counter_inst0_COUT;
  reg             _GEN_1;
  always_comb begin
    _GEN_1 = _GEN_0;
    if (BTN3)
      _GEN_1 = 1'h1;
  end // always_comb
  reg             _GEN_2;
  always_comb begin
    _GEN_2 = _GEN_1;
    if (BTN1)
      _GEN_2 = 1'h0;
  end // always_comb
  reg             Register_inst3;
  reg  [7:0]      _GEN_3;
  always_comb begin
    _GEN_3 = Register_inst0;
    if (_Counter_inst0_COUT & Register_inst3)
      _GEN_3 = _bcd8_increment_inst0_dout;
  end // always_comb
  reg  [7:0]      Register_inst1;
  reg  [7:0]      _GEN_4;
  reg  [4:0]      _GEN_5;
  always_comb begin
    _GEN_5 = _GEN;
    _GEN_4 = Register_inst1;
    if (BTN2) begin
      _GEN_4 = Register_inst0;
      _GEN_5 = 5'h14;
    end
  end // always_comb
  reg  [4:0]      Register_inst2;
  reg  [4:0]      _GEN_6;
  always_comb begin
    _GEN_6 = Register_inst2;
    if (_Counter_inst0_COUT & (|Register_inst2))
      _GEN_6 = Register_inst2 - 5'h1;
  end // always_comb
  reg  [7:0]      _GEN_7;
  always_comb begin
    _GEN_7 = _GEN_3;
    _GEN = _GEN_6;
    _GEN_0 = Register_inst3;
    if (~BTN_N) begin
      _GEN_7 = 8'h0;
      _GEN_0 = 1'h0;
      _GEN = 5'h0;
    end
  end // always_comb
  always_ff @(posedge CLK) begin
    Register_inst3 <= _GEN_2;
    Register_inst1 <= _GEN_4;
    Register_inst2 <= _GEN_5;
    Register_inst0 <= _GEN_7;
  end // always_ff @(posedge)
  initial begin
    Register_inst3 = 1'h0;
    Register_inst1 = 8'h0;
    Register_inst2 = 5'h0;
    Register_inst0 = 8'h0;
  end // initial
  wire [1:0][7:0] _GEN_8 = {{Register_inst1}, {Register_inst0}};
  Counter Counter_inst0 (
    .CLK  (CLK),
    .O    (/* unused */),
    .COUT (_Counter_inst0_COUT)
  );
  bcd8_increment bcd8_increment_inst0 (
    .din  (Register_inst0),
    .dout (_bcd8_increment_inst0_dout)
  );
  seven_seg_ctrl seven_seg_ctrl_inst0 (
    .CLK  (CLK),
    .din  (_GEN_8[|Register_inst2]),
    .dout (_seven_seg_ctrl_inst0_dout)
  );
  assign LED1 = BTN1 & BTN2;
  assign LED2 = BTN1 & BTN3;
  assign LED3 = BTN2 & BTN3;
  assign LED4 = ~BTN_N;
  assign LED5 = ~BTN_N | BTN1 | BTN2 | BTN3;
  assign P1A1 = _seven_seg_ctrl_inst0_dout[7];
  assign P1A2 = _seven_seg_ctrl_inst0_dout[6];
  assign P1A3 = _seven_seg_ctrl_inst0_dout[5];
  assign P1A4 = _seven_seg_ctrl_inst0_dout[4];
  assign P1A7 = _seven_seg_ctrl_inst0_dout[3];
  assign P1A8 = _seven_seg_ctrl_inst0_dout[2];
  assign P1A9 = _seven_seg_ctrl_inst0_dout[1];
  assign P1A10 = _seven_seg_ctrl_inst0_dout[0];
endmodule

