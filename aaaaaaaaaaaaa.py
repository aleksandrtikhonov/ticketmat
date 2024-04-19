import ctypes


lib = ctypes.CDLL("./main.so")

lib.getGoRandom.restype = ctypes.c_char_p
lib.getGoRandom.argtypes = [ctypes.c_longlong]

def get_random_from_go(seed):
    return lib.getGoRandom(seed).decode("utf-8")


# # Пример использования
# seed = 500000000
# random_number = get_random_from_go(seed)
# print("Random number from Go:", random_number)

