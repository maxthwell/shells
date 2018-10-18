
CC = g++
CFLAGS = -g3 -ggdb -gdwarf-2 -m64 -fPIC -std=c++11
LDFLAGS = -lm

all: main

main.o: main.cpp
	${CC} ${CFLAGS} -c main.cpp

main: main.o
	${CC} ${CFLAGS} main.o -L/usr/lib64 -lrados -o main
        
        


clean:
	rm -rf *.o
	rm -rf main

