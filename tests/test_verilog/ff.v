// ff.v
module FF(input clk, input rst, input d, output q);

parameter init = 0;

reg ff; 
always @(posedge clk or posedge rst) begin
  if (!rst)
    ff <= init;
  else
    ff <= d; 
end

assign q = ff;
endmodule
