module coreir_wire #(
    parameter width = 1
) (
    input [width-1:0] in,
    output [width-1:0] out
);
  assign out = in;
endmodule

module coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

endmodule

module MonitorWrapper (
    input [7:0] arr [63:0]
);
wire [7:0] _magma_inline_wire0_out;
wire [7:0] _magma_inline_wire1_out;
wire [7:0] _magma_inline_wire10_out;
wire [7:0] _magma_inline_wire11_out;
wire [7:0] _magma_inline_wire12_out;
wire [7:0] _magma_inline_wire13_out;
wire [7:0] _magma_inline_wire14_out;
wire [7:0] _magma_inline_wire15_out;
wire [7:0] _magma_inline_wire16_out;
wire [7:0] _magma_inline_wire17_out;
wire [7:0] _magma_inline_wire18_out;
wire [7:0] _magma_inline_wire19_out;
wire [7:0] _magma_inline_wire2_out;
wire [7:0] _magma_inline_wire20_out;
wire [7:0] _magma_inline_wire21_out;
wire [7:0] _magma_inline_wire22_out;
wire [7:0] _magma_inline_wire23_out;
wire [7:0] _magma_inline_wire24_out;
wire [7:0] _magma_inline_wire25_out;
wire [7:0] _magma_inline_wire26_out;
wire [7:0] _magma_inline_wire27_out;
wire [7:0] _magma_inline_wire28_out;
wire [7:0] _magma_inline_wire29_out;
wire [7:0] _magma_inline_wire3_out;
wire [7:0] _magma_inline_wire30_out;
wire [7:0] _magma_inline_wire31_out;
wire [7:0] _magma_inline_wire32_out;
wire [7:0] _magma_inline_wire33_out;
wire [7:0] _magma_inline_wire34_out;
wire [7:0] _magma_inline_wire35_out;
wire [7:0] _magma_inline_wire36_out;
wire [7:0] _magma_inline_wire37_out;
wire [7:0] _magma_inline_wire38_out;
wire [7:0] _magma_inline_wire39_out;
wire [7:0] _magma_inline_wire4_out;
wire [7:0] _magma_inline_wire40_out;
wire [7:0] _magma_inline_wire41_out;
wire [7:0] _magma_inline_wire42_out;
wire [7:0] _magma_inline_wire43_out;
wire [7:0] _magma_inline_wire44_out;
wire [7:0] _magma_inline_wire45_out;
wire [7:0] _magma_inline_wire46_out;
wire [7:0] _magma_inline_wire47_out;
wire [7:0] _magma_inline_wire48_out;
wire [7:0] _magma_inline_wire49_out;
wire [7:0] _magma_inline_wire5_out;
wire [7:0] _magma_inline_wire50_out;
wire [7:0] _magma_inline_wire51_out;
wire [7:0] _magma_inline_wire52_out;
wire [7:0] _magma_inline_wire53_out;
wire [7:0] _magma_inline_wire54_out;
wire [7:0] _magma_inline_wire55_out;
wire [7:0] _magma_inline_wire56_out;
wire [7:0] _magma_inline_wire57_out;
wire [7:0] _magma_inline_wire58_out;
wire [7:0] _magma_inline_wire59_out;
wire [7:0] _magma_inline_wire6_out;
wire [7:0] _magma_inline_wire60_out;
wire [7:0] _magma_inline_wire61_out;
wire [7:0] _magma_inline_wire62_out;
wire [7:0] _magma_inline_wire63_out;
wire [7:0] _magma_inline_wire7_out;
wire [7:0] _magma_inline_wire8_out;
wire [7:0] _magma_inline_wire9_out;
coreir_wire #(
    .width(8)
) _magma_inline_wire0 (
    .in(arr[63]),
    .out(_magma_inline_wire0_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire1 (
    .in(arr[62]),
    .out(_magma_inline_wire1_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire10 (
    .in(arr[53]),
    .out(_magma_inline_wire10_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire11 (
    .in(arr[52]),
    .out(_magma_inline_wire11_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire12 (
    .in(arr[51]),
    .out(_magma_inline_wire12_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire13 (
    .in(arr[50]),
    .out(_magma_inline_wire13_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire14 (
    .in(arr[49]),
    .out(_magma_inline_wire14_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire15 (
    .in(arr[48]),
    .out(_magma_inline_wire15_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire16 (
    .in(arr[47]),
    .out(_magma_inline_wire16_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire17 (
    .in(arr[46]),
    .out(_magma_inline_wire17_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire18 (
    .in(arr[45]),
    .out(_magma_inline_wire18_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire19 (
    .in(arr[44]),
    .out(_magma_inline_wire19_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire2 (
    .in(arr[61]),
    .out(_magma_inline_wire2_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire20 (
    .in(arr[43]),
    .out(_magma_inline_wire20_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire21 (
    .in(arr[42]),
    .out(_magma_inline_wire21_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire22 (
    .in(arr[41]),
    .out(_magma_inline_wire22_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire23 (
    .in(arr[40]),
    .out(_magma_inline_wire23_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire24 (
    .in(arr[39]),
    .out(_magma_inline_wire24_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire25 (
    .in(arr[38]),
    .out(_magma_inline_wire25_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire26 (
    .in(arr[37]),
    .out(_magma_inline_wire26_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire27 (
    .in(arr[36]),
    .out(_magma_inline_wire27_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire28 (
    .in(arr[35]),
    .out(_magma_inline_wire28_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire29 (
    .in(arr[34]),
    .out(_magma_inline_wire29_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire3 (
    .in(arr[60]),
    .out(_magma_inline_wire3_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire30 (
    .in(arr[33]),
    .out(_magma_inline_wire30_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire31 (
    .in(arr[32]),
    .out(_magma_inline_wire31_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire32 (
    .in(arr[31]),
    .out(_magma_inline_wire32_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire33 (
    .in(arr[30]),
    .out(_magma_inline_wire33_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire34 (
    .in(arr[29]),
    .out(_magma_inline_wire34_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire35 (
    .in(arr[28]),
    .out(_magma_inline_wire35_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire36 (
    .in(arr[27]),
    .out(_magma_inline_wire36_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire37 (
    .in(arr[26]),
    .out(_magma_inline_wire37_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire38 (
    .in(arr[25]),
    .out(_magma_inline_wire38_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire39 (
    .in(arr[24]),
    .out(_magma_inline_wire39_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire4 (
    .in(arr[59]),
    .out(_magma_inline_wire4_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire40 (
    .in(arr[23]),
    .out(_magma_inline_wire40_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire41 (
    .in(arr[22]),
    .out(_magma_inline_wire41_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire42 (
    .in(arr[21]),
    .out(_magma_inline_wire42_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire43 (
    .in(arr[20]),
    .out(_magma_inline_wire43_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire44 (
    .in(arr[19]),
    .out(_magma_inline_wire44_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire45 (
    .in(arr[18]),
    .out(_magma_inline_wire45_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire46 (
    .in(arr[17]),
    .out(_magma_inline_wire46_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire47 (
    .in(arr[16]),
    .out(_magma_inline_wire47_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire48 (
    .in(arr[15]),
    .out(_magma_inline_wire48_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire49 (
    .in(arr[14]),
    .out(_magma_inline_wire49_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire5 (
    .in(arr[58]),
    .out(_magma_inline_wire5_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire50 (
    .in(arr[13]),
    .out(_magma_inline_wire50_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire51 (
    .in(arr[12]),
    .out(_magma_inline_wire51_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire52 (
    .in(arr[11]),
    .out(_magma_inline_wire52_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire53 (
    .in(arr[10]),
    .out(_magma_inline_wire53_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire54 (
    .in(arr[9]),
    .out(_magma_inline_wire54_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire55 (
    .in(arr[8]),
    .out(_magma_inline_wire55_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire56 (
    .in(arr[7]),
    .out(_magma_inline_wire56_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire57 (
    .in(arr[6]),
    .out(_magma_inline_wire57_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire58 (
    .in(arr[5]),
    .out(_magma_inline_wire58_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire59 (
    .in(arr[4]),
    .out(_magma_inline_wire59_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire6 (
    .in(arr[57]),
    .out(_magma_inline_wire6_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire60 (
    .in(arr[3]),
    .out(_magma_inline_wire60_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire61 (
    .in(arr[2]),
    .out(_magma_inline_wire61_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire62 (
    .in(arr[1]),
    .out(_magma_inline_wire62_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire63 (
    .in(arr[0]),
    .out(_magma_inline_wire63_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire7 (
    .in(arr[56]),
    .out(_magma_inline_wire7_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire8 (
    .in(arr[55]),
    .out(_magma_inline_wire8_out)
);
coreir_wire #(
    .width(8)
) _magma_inline_wire9 (
    .in(arr[54]),
    .out(_magma_inline_wire9_out)
);

monitor #(.WIDTH(8), .DEPTH(64)) monitor_inst(.arr('{_magma_inline_wire0_out, _magma_inline_wire1_out, _magma_inline_wire2_out, _magma_inline_wire3_out, _magma_inline_wire4_out, _magma_inline_wire5_out, _magma_inline_wire6_out, _magma_inline_wire7_out, _magma_inline_wire8_out, _magma_inline_wire9_out, _magma_inline_wire10_out, _magma_inline_wire11_out, _magma_inline_wire12_out, _magma_inline_wire13_out, _magma_inline_wire14_out, _magma_inline_wire15_out, _magma_inline_wire16_out, _magma_inline_wire17_out, _magma_inline_wire18_out, _magma_inline_wire19_out, _magma_inline_wire20_out, _magma_inline_wire21_out, _magma_inline_wire22_out, _magma_inline_wire23_out, _magma_inline_wire24_out, _magma_inline_wire25_out, _magma_inline_wire26_out, _magma_inline_wire27_out, _magma_inline_wire28_out, _magma_inline_wire29_out, _magma_inline_wire30_out, _magma_inline_wire31_out, _magma_inline_wire32_out, _magma_inline_wire33_out, _magma_inline_wire34_out, _magma_inline_wire35_out, _magma_inline_wire36_out, _magma_inline_wire37_out, _magma_inline_wire38_out, _magma_inline_wire39_out, _magma_inline_wire40_out, _magma_inline_wire41_out, _magma_inline_wire42_out, _magma_inline_wire43_out, _magma_inline_wire44_out, _magma_inline_wire45_out, _magma_inline_wire46_out, _magma_inline_wire47_out, _magma_inline_wire48_out, _magma_inline_wire49_out, _magma_inline_wire50_out, _magma_inline_wire51_out, _magma_inline_wire52_out, _magma_inline_wire53_out, _magma_inline_wire54_out, _magma_inline_wire55_out, _magma_inline_wire56_out, _magma_inline_wire57_out, _magma_inline_wire58_out, _magma_inline_wire59_out, _magma_inline_wire60_out, _magma_inline_wire61_out, _magma_inline_wire62_out, _magma_inline_wire63_out}));
                    
endmodule

