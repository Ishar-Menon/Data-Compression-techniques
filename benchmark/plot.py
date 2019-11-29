import numpy as np
import matplotlib.pyplot as plt





original = np.array([251000, 502000, 753000, 1004000, 1255000, 1506000, 1757000, 2008000, 2259000, 2510000])
lzw = np.array([0.30, 0.58, 0.86, 1.16, 1.43, 1.79, 2.03, 2.25, 2.57, 2.83])
huffman = np.array([0.25, 0.50, 0.77, 1.00, 1.28, 1.58, 1.75, 2.18, 2.26, 2.53])




plt.title("Time Comparison - LZW vs Huffman ", fontsize = 30)
plt.rcParams["figure.figsize"] = (20, 10)
plt.ylabel("Time taken in seconds", fontsize = 25)
plt.xlabel("Size of input file in bytes", fontsize = 25)


# plt.plot(original, "-o")
plt.plot(original ,lzw,"-o")
plt.plot(original,huffman,"-o")

plt.legend(['LZW', 'Huffman'], loc = 'upper left', prop = {'size' : 20})

plt.show()