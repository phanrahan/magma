// Module `MyCircuit` defined externally
module Top (
    output IFC1_port4
);
wire [4:0] MyCircuit_inst0_IFC0_port0;
wire [4:0] MyCircuit_inst0_IFC0_port1;
wire [2:0] MyCircuit_inst0_IFC0_port10;
wire [1:0] MyCircuit_inst0_IFC0_port2 [4:0];
wire [4:0] MyCircuit_inst0_IFC0_port3;
wire MyCircuit_inst0_IFC0_port4;
wire MyCircuit_inst0_IFC0_port5;
wire MyCircuit_inst0_IFC0_port7;
wire MyCircuit_inst0_IFC0_port8;
wire MyCircuit_inst0_IFC0_port9;
MyCircuit MyCircuit_inst0 (
    .IFC0_port0(MyCircuit_inst0_IFC0_port0),
    .IFC0_port1(MyCircuit_inst0_IFC0_port1),
    .IFC0_port10(MyCircuit_inst0_IFC0_port10),
    .IFC0_port2(MyCircuit_inst0_IFC0_port2),
    .IFC0_port3(MyCircuit_inst0_IFC0_port3),
    .IFC0_port4(MyCircuit_inst0_IFC0_port4),
    .IFC0_port5(MyCircuit_inst0_IFC0_port5),
    .IFC0_port7(MyCircuit_inst0_IFC0_port7),
    .IFC0_port8(MyCircuit_inst0_IFC0_port8),
    .IFC0_port9(MyCircuit_inst0_IFC0_port9)
);
assign IFC1_port4 = MyCircuit_inst0_IFC0_port4;
endmodule

