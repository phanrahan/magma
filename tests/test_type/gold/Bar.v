// Module `Foo` defined externally
module Bar (input ASYNCRESETN, input CLK);
Foo Foo_inst0(.ASYNCRESETN(ASYNCRESETN), .CLK(CLK));
endmodule

