module corebit_term (
    input in
);

endmodule

module Passthru_unq1 (
    input I,
    output O
);
assign O = I;

initial begin
    $display("Id = %d", 1);
end
                    
endmodule

module Passthru (
    input I,
    output O
);
assign O = I;

initial begin
    $display("Id = %d", 0);
end
                    
endmodule

module Top (
    input I,
    output O
);
wire Passthru_inst0_O;
Passthru Passthru_inst0 (
    .I(I),
    .O(Passthru_inst0_O)
);
Passthru_unq1 Passthru_inst1 (
    .I(Passthru_inst0_O),
    .O(O)
);
endmodule

