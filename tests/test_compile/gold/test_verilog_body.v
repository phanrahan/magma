module baz_Foo (
    input I,
    output O
);

always @(*) begin
    O = I;
    // Note we need to escape the newline here or python treats it as regular
    // newline
    $display("%d\n", I);
end

endmodule

