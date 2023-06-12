"""
helper functions to get COVG data to work with abfWriter
Lucas Koerner 6/2023
koerner.lucas@stthomas.edu
"""

import numpy as np

def interleave_np(l_arr):
    # interleave multiple arrays before writing ABF 
    # l_arr: list of arrays (all same length)
    sz = [a.size for a in l_arr]
    print(sz)
    if not all(x==sz[0] for x in sz):
        print('Error list of arrays must all have the same length')
        return -1
    composite = np.empty((1,np.sum(sz)), dtype=l_arr[0].dtype)
    num_el = len(l_arr)
    for idx, a in enumerate(l_arr):
        composite[0,idx::num_el] = a
    return composite


if __name__ == "__main__":
    print("DO NOT RUN THIS FILE DIRECTLY")