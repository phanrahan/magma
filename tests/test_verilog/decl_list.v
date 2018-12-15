module memory_core(clk_in, clk_en, reset, config_addr, config_data,
     config_read, config_write, config_en, config_en_sram,
     config_en_linebuf, data_in, data_out, wen_in, ren_in, valid_out,
     chain_in, chain_out, chain_wen_in, chain_valid_out, almost_full,
     almost_empty, addr_in, read_data, read_data_sram,
     read_data_linebuf, flush);
  input clk_in, clk_en, reset, config_read, config_write, config_en,
       config_en_linebuf, wen_in, ren_in, chain_wen_in, flush;
  input [31:0] config_addr, config_data;
  input [3:0] config_en_sram;
  input [15:0] data_in, chain_in, addr_in;
  output [15:0] data_out, chain_out;
  output valid_out, chain_valid_out, almost_full, almost_empty;
  output [31:0] read_data, read_data_sram, read_data_linebuf;
endmodule
