module VerilogFSM(input frameValid, input clk, input rst, input real_href, output pixel_valid);
    localparam IDLE=2'h0, HBLANK=2'h1, HACT=2'h2, PIX_PER_LINE=120;
    reg [10:0] pix_cnt_n;
    reg [10:0] pix_cnt;

    reg [1:0] pix_ns;
    reg [1:0] pix_cs;

    assign pixel_valid = (pix_cs == HACT);
    always @(*) begin
        case(pix_cs)
            IDLE : begin
                pix_ns = frameValid ? HBLANK : IDLE;
                pix_cnt_n = 0;
            end
            HBLANK : begin
                pix_ns = real_href ? HACT : HBLANK ;
                pix_cnt_n = real_href ? PIX_PER_LINE : 0;
            end
            HACT : begin
                pix_ns = (pix_cnt == 1) ? HBLANK : HACT ;
                pix_cnt_n = pix_cnt - 1'b1;
            end
            default : begin
                pix_ns = IDLE ;
                pix_cnt_n = 0;
            end
        endcase

    end
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            pix_cs <= IDLE;
            pix_cnt <= 0;
        end else begin
            pix_cs <= pix_ns;
            pix_cnt <= pix_cnt_n;
        end
    end
endmodule
