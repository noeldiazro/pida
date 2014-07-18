all: nanosleep_jitter interrupt

nanosleep_jitter: nanosleep_jitter.o tsop.o
	gcc -o nanosleep_jitter nanosleep_jitter.o tsop.o -lrt

nanosleep_jitter.o: nanosleep_jitter.c tsop.h
	gcc -c nanosleep_jitter.c -lrt

tsop.o: tsop.c tsop.h
	gcc -c tsop.c

interrupt: interrupt.o tsop.o
	gcc -o interrupt interrupt.o tsop.o -lwiringPi -lrt

interrupt.o: interrupt.c tsop.h
	gcc -c interrupt.c
