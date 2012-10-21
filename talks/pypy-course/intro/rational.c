#include <stdio.h>

int main()
{
    float px = 0.0, py = 0.0;
    while (px < 2000.0) {
        px += 1.0;
        py += 0.5;
    }
    printf("%f %f\n", px, py);
}
