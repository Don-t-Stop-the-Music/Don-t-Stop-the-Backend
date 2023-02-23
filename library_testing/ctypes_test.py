# ctypes_test.py
import ctypes

if __name__ == "__main__":
    # Load the shared library into ctypes
    c_lib = ctypes.CDLL("c_lib/c_lib.so")

    # Use function in libarary
    print(c_lib.cmult(2,3))