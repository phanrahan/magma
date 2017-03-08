module main_tb;

   // initial values
   reg I = 0;
   wire O;

   initial
     begin
        $dumpfile("inout1.vcd");
        $dumpvars(0, inst);

        #1 I = 1'b1;
        $finish;
     end

   main inst(I, O);
endmodule
