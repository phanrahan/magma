module mod1 #(parameter KRATOS_INSTANCE_ID = 'h1)
(
    input I
);

endmodule   // mod
module mod0 #(parameter KRATOS_INSTANCE_ID = 32'h0)
(
    input I
);

endmodule   // mod
module Top (input I);
mod0 #(.KRATOS_INSTANCE_ID(0)) mod0_inst0(.I(I));
mod0 #(.KRATOS_INSTANCE_ID(1)) mod0_inst1(.I(I));
mod1 #(.KRATOS_INSTANCE_ID(1)) mod1_inst0(.I(I));
mod1 #(.KRATOS_INSTANCE_ID(7)) mod1_inst1(.I(I));
endmodule

