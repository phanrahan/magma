module monitor #(
    parameter WIDTH = 64, 
    parameter DEPTH = 32
) (
    input [WIDTH - 1:0] arr [DEPTH - 1:0]
);

always @(*) begin
    for (integer i = 0; i < DEPTH; i++) begin
        $display("arr[%d]=%x", i, arr[i]);
    end
end
endmodule
