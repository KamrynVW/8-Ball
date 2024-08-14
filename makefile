CC = clang
CFLAGS = -Wall -std=c99 -pedantic

all: _phylib.so

clean:
	rm -f *.o *.so *.svg *.db phylib_wrap.c phylib.py -r __pycache__

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -fPIC -c -o phylib.o phylib.c

libphylib.so: phylib.o
	$(CC) phylib.o -shared -o libphylib.so

phylib_wrap.c: phylib.i libphylib.so
	swig -python phylib.i

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -I/usr/include/python3.11/ -fPIC -o phylib_wrap.o

_phylib.so: phylib_wrap.o
	$(CC) $(CFLAGS) -shared phylib_wrap.o -L. -L/usr/lib/python3.11 -lpython3.11 -lphylib -o _phylib.so