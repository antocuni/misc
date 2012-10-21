// A safe array example.
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

class Array2D {
  double *data;
public:
  int width, height;
  Array2D(int w, int h) {
    width = w;
    height = h;
    data = (double *) malloc(w*h*sizeof(double));
  }
  double &operator()(int x, int y) {
    if (x >= 0 && x < width && y >= 0 && y < height) {
	return data[y*width + x];
    }
    printf("IndexError\n");
    exit(1);
  }
};

void sobel_magnitude(Array2D &a, Array2D &b) {
  int x, y;
  for (y=1; y<a.height-1; y++) {
    for (x=1; x<a.width-1; x++) {
      double dx = -1.0*a(x-1, y-1) + 1.0*a(x+1, y-1) +
	          -2.0*a(x-1, y)   + 2.0*a(x+1, y)   + 
	          -1.0*a(x-1, y+1) + 1.0*a(x+1, y+1);

      double dy = -1.0*a(x-1, y-1) - 2.0*a(x, y-1) - 1.0*a(x+1, y-1) +
	           1.0*a(x-1, y+1) + 2.0*a(x, y+1) + 1.0*a(x+1, y+1);
      b(x, y) = sqrt(dx*dx + dy*dy) / 4.0;

    }
  }
}

int main(int ac, char **av) {
  int w = atoi(av[1]), h = atoi(av[2]);
  int i;

  for (i=0; i<10; i++) {
    Array2D a(w, h), b(w, h);
    sobel_magnitude(a, b);
    printf("%f\n", b(1,1));
  }
  fprintf(stderr, "sobel(Array2D(%dx%d)):  ", w, h);
  return 0;
}
