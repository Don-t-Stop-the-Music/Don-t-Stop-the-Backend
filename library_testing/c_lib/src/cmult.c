#include <stdio.h>

int cmult(int x, int y) {
    int return_value = x * y;
    printf("    In cmult : int: %d int %d returning  %d\n", x, y, return_value);
    return return_value;
}