module TestReadyValidTuple (
    input I_data__0,
    input [4:0] I_data__1,
    output I_ready,
    input I_valid,
    output O_data__0,
    output [4:0] O_data__1,
    input O_ready,
    output O_valid
);
assign I_ready = O_ready;
assign O_data__0 = I_data__0;
assign O_data__1 = I_data__1;
assign O_valid = I_valid;
endmodule

