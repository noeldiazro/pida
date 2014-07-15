all: nanosleep_jitter

nanosleep_jitter: nanosleep_jitter.o tsop.o
	gcc -o nanosleep_jitter nanosleep_jitter.o tsop.o -lrt

nanosleep_jitter.o: nanosleep_jitter.c tsop.h
	gcc -c nanosleep_jitter.c -lrt

tsop.o: tsop.c tsop.h
	gcc -c tsop.c