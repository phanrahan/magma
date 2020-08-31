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
mod0 #(
    .KRATOS_INSTANCE_ID(-559038737)
) mod0_inst0 (
    .I(I)
);
mod0 #(
    .KRATOS_INSTANCE_ID(-559038737)
) mod0_inst1 (
    .I(I)
);
mod1 #(
    .KRATOS_INSTANCE_ID(239)
) mod1_inst0 (
    .I(I)
);
mod1 #(
    .KRATOS_INSTANCE_ID(239)
) mod1_inst1 (
    .I(I)
);
mod2 #(
    .KRATOS_INSTANCE_ID(23)
) mod2_inst0 (
    .I(I)
);
mod2 #(
    .KRATOS_INSTANCE_ID(23)
) mod2_inst1 (
    .I(I)
);
mod3 #(
    .KRATOS_INSTANCE_ID(23)
) mod3_inst0 (
    .I(I)
);
mod3 #(
    .KRATOS_INSTANCE_ID(23)
) mod3_inst1 (
    .I(I)
);
mod4 #(
    .KRATOS_INSTANCE_ID(482)
) mod4_inst0 (
    .I(I)
);
mod4 #(
    .KRATOS_INSTANCE_ID(482)
) mod4_inst1 (
    .I(I)
);
mod5 #(
    .KRATOS_INSTANCE_ID(17)
) mod5_inst0 (
    .I(I)
);
mod5 #(
    .KRATOS_INSTANCE_ID(17)
) mod5_inst1 (
    .I(I)
);
endmodule

