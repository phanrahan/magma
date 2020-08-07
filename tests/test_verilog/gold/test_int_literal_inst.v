module mod5 #(parameter KRATOS_INSTANCE_ID = 17)
(
    input I
);

endmodule   // mod
module mod4 #(parameter KRATOS_INSTANCE_ID = 13'o742)
(
    input I
);

endmodule   // mod
module mod3 #(parameter KRATOS_INSTANCE_ID = 16'b10111)
(
    input I
);

endmodule   // mod
module mod2 #(parameter KRATOS_INSTANCE_ID = 24'sd23)
(
    input I
);

endmodule   // mod
module mod1 #(parameter KRATOS_INSTANCE_ID = 'hEF)
(
    input I
);

endmodule   // mod
module mod0 #(parameter KRATOS_INSTANCE_ID = 32'hDEADBEEF)
(
    input I
);

endmodule   // mod
module Top (
    input I
);
wire mod0_inst0_I;
wire mod0_inst1_I;
wire mod1_inst0_I;
wire mod1_inst1_I;
wire mod2_inst0_I;
wire mod2_inst1_I;
wire mod3_inst0_I;
wire mod3_inst1_I;
wire mod4_inst0_I;
wire mod4_inst1_I;
wire mod5_inst0_I;
wire mod5_inst1_I;
assign mod0_inst0_I = I;
mod0 #(
    .KRATOS_INSTANCE_ID(-559038737)
) mod0_inst0 (
    .I(mod0_inst0_I)
);
assign mod0_inst1_I = I;
mod0 #(
    .KRATOS_INSTANCE_ID(-559038737)
) mod0_inst1 (
    .I(mod0_inst1_I)
);
assign mod1_inst0_I = I;
mod1 #(
    .KRATOS_INSTANCE_ID(239)
) mod1_inst0 (
    .I(mod1_inst0_I)
);
assign mod1_inst1_I = I;
mod1 #(
    .KRATOS_INSTANCE_ID(239)
) mod1_inst1 (
    .I(mod1_inst1_I)
);
assign mod2_inst0_I = I;
mod2 #(
    .KRATOS_INSTANCE_ID(23)
) mod2_inst0 (
    .I(mod2_inst0_I)
);
assign mod2_inst1_I = I;
mod2 #(
    .KRATOS_INSTANCE_ID(23)
) mod2_inst1 (
    .I(mod2_inst1_I)
);
assign mod3_inst0_I = I;
mod3 #(
    .KRATOS_INSTANCE_ID(23)
) mod3_inst0 (
    .I(mod3_inst0_I)
);
assign mod3_inst1_I = I;
mod3 #(
    .KRATOS_INSTANCE_ID(23)
) mod3_inst1 (
    .I(mod3_inst1_I)
);
assign mod4_inst0_I = I;
mod4 #(
    .KRATOS_INSTANCE_ID(482)
) mod4_inst0 (
    .I(mod4_inst0_I)
);
assign mod4_inst1_I = I;
mod4 #(
    .KRATOS_INSTANCE_ID(482)
) mod4_inst1 (
    .I(mod4_inst1_I)
);
assign mod5_inst0_I = I;
mod5 #(
    .KRATOS_INSTANCE_ID(17)
) mod5_inst0 (
    .I(mod5_inst0_I)
);
assign mod5_inst1_I = I;
mod5 #(
    .KRATOS_INSTANCE_ID(17)
) mod5_inst1 (
    .I(mod5_inst1_I)
);
endmodule

