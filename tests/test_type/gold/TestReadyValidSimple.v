module TestReadyValidSimple (
    input [4:0] I_data,
    output I_ready,
    input I_valid,
    output [4:0] O_data,
    input O_ready,
    output O_valid,
    output fired
);
assign I_ready = O_ready;
assign O_data = I_data;
assign O_valid = I_valid;
assign fired = (O_ready & I_valid) & (O_ready & I_valid);
endmodule

