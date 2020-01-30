module RTLMonitor (input CLK, input handshake_arr_0_ready, input handshake_arr_0_valid, input handshake_arr_1_ready, input handshake_arr_1_valid, input handshake_arr_2_ready, input handshake_arr_2_valid, input handshake_ready, input handshake_valid, input [3:0] in1, input [3:0] in2, input intermediate_tuple__0, input intermediate_tuple__1, input mon_temp1, input mon_temp2, input out);

                    logic temp1, temp2;
                    assign temp1 = |(in1);
                    assign temp2 = &(in1);
                    assert property (@(posedge CLK) handshake_valid -> out === temp1 && temp2);
                
endmodule


bind RTL RTLMonitor RTLMonitor_inst (.CLK(CLK), .in1(in1), .in2(in2), .out(out), .handshake_ready(handshake_ready), .handshake_valid(handshake_valid), .handshake_arr_0_ready(handshake_arr_0_ready), .handshake_arr_0_valid(handshake_arr_0_valid), .handshake_arr_1_ready(handshake_arr_1_ready), .handshake_arr_1_valid(handshake_arr_1_valid), .handshake_arr_2_ready(handshake_arr_2_ready), .handshake_arr_2_valid(handshake_arr_2_valid), .mon_temp1(orr_4_inst0.O), .mon_temp2(andr_4_inst0.O));