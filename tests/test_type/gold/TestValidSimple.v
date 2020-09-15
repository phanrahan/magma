module TestValidSimple (
    input [4:0] I_data,
    input I_valid,
    output [4:0] O_data,
    output O_valid
);
assign O_data = I_data;
assign O_valid = I_valid;
endmodule

