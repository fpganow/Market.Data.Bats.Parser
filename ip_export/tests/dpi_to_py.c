#include "svdpi.h"
#include <stdio.h>

DPI_DLLESPEC
int dpi_function(const svOpenArrayHandle v, const svOpenArrayHandle v_out)
{
    int out_sum = 0;

    int l1 = svLow(v, 1);
    int h1 = svHigh(v, 1);
    for(int i = l1; i<= h1; i++) {
        printf("\t%d", *((char*)svGetArrElemPtr1(v, i)));
        out_sum += *((char*)svGetArrElemPtr1(v, i));
    }
    printf("\n\n");

    int v_l = svLow(v_out, 1);
    int v_h = svHigh(v_out, 1);
    printf(" - v_low: %d\n", v_l);
    printf(" - v_high: %d\n", v_h);
    *((char*)svGetArrElemPtr1(v_out, 0)) = 100;
    *((char*)svGetArrElemPtr1(v_out, 1)) = 200;
    *((char*)svGetArrElemPtr1(v_out, 2)) = 300;

    return out_sum;
}
