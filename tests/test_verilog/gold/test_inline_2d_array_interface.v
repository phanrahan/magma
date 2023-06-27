module coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

endmodule

module MonitorWrapper (
    input [7:0] arr [63:0]
);

monitor #(.WIDTH(8), .DEPTH(64)) monitor_inst(.arr('{arr[63], arr[62], arr[61], arr[60], arr[59], arr[58], arr[57], arr[56], arr[55], arr[54], arr[53], arr[52], arr[51], arr[50], arr[49], arr[48], arr[47], arr[46], arr[45], arr[44], arr[43], arr[42], arr[41], arr[40], arr[39], arr[38], arr[37], arr[36], arr[35], arr[34], arr[33], arr[32], arr[31], arr[30], arr[29], arr[28], arr[27], arr[26], arr[25], arr[24], arr[23], arr[22], arr[21], arr[20], arr[19], arr[18], arr[17], arr[16], arr[15], arr[14], arr[13], arr[12], arr[11], arr[10], arr[9], arr[8], arr[7], arr[6], arr[5], arr[4], arr[3], arr[2], arr[1], arr[0]}));
                    
endmodule

