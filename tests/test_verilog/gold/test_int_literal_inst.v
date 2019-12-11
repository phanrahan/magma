module mod5 #(parameter KRATOS_INSTANCE_ID = 17)
(
    input I
);

endmodule   // mod
module mod4 #(parameter KRATOS_INSTANCE_ID = 13'o7)
(
    input I
);

endmodule   // mod
module mod3 #(parameter KRATOS_INSTANCE_ID = 16'b1)
(
    input I
);

endmodule   // mod
module mod2 #(parameter KRATOS_INSTANCE_ID = 24'sd2)
(
    input I
);

endmodule   // mod
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
mod0 mod0_inst0(.I(I));
mod1 mod1_inst0(.I(I));
mod2 mod2_inst0(.I(I));
mod3 mod3_inst0(.I(I));
mod4 mod4_inst0(.I(I));
mod5 mod5_inst0(.I(I));
endmodule

