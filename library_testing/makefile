ctypes_test:

	gcc -c -fPIC c_lib/src/cmult.c  -o c_lib/bin/cmult.o 
#making object file

	gcc -shared c_lib/bin/cmult.o  -o c_lib/c_lib.so
#linking single object file to shared library (can do more: gcc -shared c_lib/bin/cmult.o c_lib/bin/cadd.o   -o c_lib/c_lib.so)

	python ctypes_test.py
#running python


