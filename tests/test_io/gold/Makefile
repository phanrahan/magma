NAME = inout1

all : $(NAME).vcd

$(NAME).vcd : $(NAME)_tb.v $(NAME).v
	rm -f $(NAME).vcd
	iverilog -o $(NAME).vvp $(NAME)_tb.v $(NAME).v
	./$(NAME).vvp 

clean :
	rm -f $(NAME).vcd
	rm -f $(NAME).vvp

