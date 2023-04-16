int factorial(int n) {
    int result = 1;

    for(int i=1; i<n+1; i++) {
        result *= i;
    }

    return result;
}

/*
#include <stdio.h>
int main(void) {
    for(int i=0; i<10; i++) {
        printf("fac(%d) = %d\n", i, factorial(i));
    }
}
*/
