CC = clang
CFLAGS = -Wall -std=c99 -pedantic

_molecule.so: libmol.so molecule_wrap.o
	$(CC) -shared molecule_wrap.o -L/usr/lib/python3.7/config3.7m-x86_64-linux-gnu -lpython3.7m -L. -lmol -o _molecule.so 

molecule_wrap.o: molecule_wrap.c
	$(CC) $(CFLAGS) -fPIC -I/usr/include/python3.7m -c molecule_wrap.c

molecule_wrap.c: molecule.i
	swig3.0 -python molecule.i

libmol.so: mol.o
	$(CC) -shared mol.o -o libmol.so -lm

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -fpic -c mol.c 

clean:
	rm -f *.o *.so molecule_wrap.c molecule.py a.out
