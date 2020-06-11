module coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

endmodule

module MonitorWrapper (
    input [7:0] arr_0,
    input [7:0] arr_1,
    input [7:0] arr_10,
    input [7:0] arr_11,
    input [7:0] arr_12,
    input [7:0] arr_13,
    input [7:0] arr_14,
    input [7:0] arr_15,
    input [7:0] arr_16,
    input [7:0] arr_17,
    input [7:0] arr_18,
    input [7:0] arr_19,
    input [7:0] arr_2,
    input [7:0] arr_20,
    input [7:0] arr_21,
    input [7:0] arr_22,
    input [7:0] arr_23,
    input [7:0] arr_24,
    input [7:0] arr_25,
    input [7:0] arr_26,
    input [7:0] arr_27,
    input [7:0] arr_28,
    input [7:0] arr_29,
    input [7:0] arr_3,
    input [7:0] arr_30,
    input [7:0] arr_31,
    input [7:0] arr_32,
    input [7:0] arr_33,
    input [7:0] arr_34,
    input [7:0] arr_35,
    input [7:0] arr_36,
    input [7:0] arr_37,
    input [7:0] arr_38,
    input [7:0] arr_39,
    input [7:0] arr_4,
    input [7:0] arr_40,
    input [7:0] arr_41,
    input [7:0] arr_42,
    input [7:0] arr_43,
    input [7:0] arr_44,
    input [7:0] arr_45,
    input [7:0] arr_46,
    input [7:0] arr_47,
    input [7:0] arr_48,
    input [7:0] arr_49,
    input [7:0] arr_5,
    input [7:0] arr_50,
    input [7:0] arr_51,
    input [7:0] arr_52,
    input [7:0] arr_53,
    input [7:0] arr_54,
    input [7:0] arr_55,
    input [7:0] arr_56,
    input [7:0] arr_57,
    input [7:0] arr_58,
    input [7:0] arr_59,
    input [7:0] arr_6,
    input [7:0] arr_60,
    input [7:0] arr_61,
    input [7:0] arr_62,
    input [7:0] arr_63,
    input [7:0] arr_7,
    input [7:0] arr_8,
    input [7:0] arr_9
);

monitor #(.WIDTH(8), .DEPTH(64)) monitor_inst(.arr('{arr_63, arr_62, arr_61, arr_60, arr_59, arr_58, arr_57, arr_56, arr_55, arr_54, arr_53, arr_52, arr_51, arr_50, arr_49, arr_48, arr_47, arr_46, arr_45, arr_44, arr_43, arr_42, arr_41, arr_40, arr_39, arr_38, arr_37, arr_36, arr_35, arr_34, arr_33, arr_32, arr_31, arr_30, arr_29, arr_28, arr_27, arr_26, arr_25, arr_24, arr_23, arr_22, arr_21, arr_20, arr_19, arr_18, arr_17, arr_16, arr_15, arr_14, arr_13, arr_12, arr_11, arr_10, arr_9, arr_8, arr_7, arr_6, arr_5, arr_4, arr_3, arr_2, arr_1, arr_0}));
                    
endmodule

