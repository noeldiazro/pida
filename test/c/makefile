all: nanosleep_jitter

nanosleep_jitter: nanosleep_jitter.o
	gcc -o nanosleep_jitter nanosleep_jitter.o -lrt

nanosleep_jitter.o: nanosleep_jitter.c
	gcc -c nanosleep_jitter.c -lrt
