module top(a, b, c);
    input a;
    output b;
    inout c;
    assign a = b & c;
endmodule
