import os
from time import perf_counter

start = perf_counter()
os.system("python processing/load.py")
os.system("python processing/clean.py")

print("Execution Time: {} minutes".format(round((perf_counter() - start) / 60, 1)))
