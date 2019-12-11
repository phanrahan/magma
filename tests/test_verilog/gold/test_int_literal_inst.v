    module mod #(parameter KRATOS_INSTANCE_ID = 32'h0)
    (
        input I
    );

    endmodule   // mod
module Top (input I);
mod mod_inst0(.I(I));
endmodule

