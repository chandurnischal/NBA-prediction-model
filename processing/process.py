import os
from time import perf_counter

start = perf_counter()
os.system("python processing/load.py")
os.system("python processing/clean.py")
os.system('python processing/toCSV.py')

print('Execution Time: {}s'.format(perf_counter() - start))