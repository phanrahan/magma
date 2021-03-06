import magma as m
import magma.testing


def test_2d_array_from_verilog():
    main = m.define_from_verilog(f"""
module transpose_buffer (
  input logic clk,
  output logic [2:0] index_inner,
  output logic [2:0] index_outer,
  input logic [3:0] input_data [63:0],
  input logic [2:0] range_inner,
  input logic [2:0] range_outer,
  input logic rst_n,
  input logic [2:0] stride
);


always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    index_outer <= 3'h0;
    index_inner <= 3'h0;
  end
  else begin
    if (index_outer == (range_outer - 3'h1)) begin
      index_outer <= 3'h0;
    end
    else index_outer <= index_outer + 3'h1;
    if (index_inner == (range_inner - 3'h1)) begin
      index_inner <= 3'h0;
    end
    else index_inner <= index_inner + 3'h1;
  end
end
endmodule   // transpose_buffer
""")[0]
    m.compile("build/2d_array_from_verilog", main, output="verilog")
    assert m.testing.check_files_equal(__file__,
                                       f"build/2d_array_from_verilog.v",
                                       f"gold/2d_array_from_verilog.v")
