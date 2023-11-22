#include "svdpi.h"

DPI_DLLESPEC
int myFunction(const svOpenArrayHandle v)
{
    int out_sum = 0;

    int l1 = svLow(v, 1);
    int h1 = svHigh(v, 1);
    for(int i = l1; i<= h1; i++) {
        printf("\t%d", *((char*)svGetArrElemPtr1(v, i)));
        out_sum += (int)svGetArrElemPtr1(v, i);
    }
    printf("\n");

    return out_sum;
}


