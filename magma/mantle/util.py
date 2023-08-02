def ispow2(n):
    return (n & (n - 1) == 0) and n != 0
