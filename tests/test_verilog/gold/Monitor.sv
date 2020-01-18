module Monitor (input  CLK, input [3:0] in1, input [3:0] in2, input  out, input  mon_temp1, input  mon_temp2);

                        logic temp1, temp2;
                        assign temp1 = |(in1);
                        assign temp2 = &(in1);
                        assert property (@(posedge CLK) out === temp1 && temp2);
                    
endmodule


bind RTL Monitor Monitor_inst (.CLK(CLK), .in1(in1), .in2(in2), .out(out), .mon_temp1(orr_4_inst0.O), .mon_temp2(andr_4_inst0.O));