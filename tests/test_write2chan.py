import numpy as np
import sys
import os 

'''
Run from pyABF as %run tests/test_write2chan.py 
Lucas Koerner, 2023/4/10 
'''

PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_PROJECT = os.path.abspath(PATH_HERE+"/../")
PATH_DATA = os.path.abspath(PATH_PROJECT+"/data/abfs/")
PATH_HEADERS = os.path.abspath(PATH_PROJECT+"/data/headers/")

try:
    # this ensures pyABF is imported from this specific path
    sys.path.insert(0, "src")
    import pyabf 
except:
    raise ImportError("couldn't import local pyABF")

abf_f = 'test65.abf'

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

from pyabf.abfWriter import writeABF1
x = np.vstack((np.linspace(0,3,512*8), np.linspace(0,33,512*8))) # this creates two sweeps 
# need to interleave 2 channels 
comp = interleave_np([x[0,:],x[1,:]])
writeABF1(comp, os.path.join(PATH_DATA, abf_f), 1e6, units=['V', 'pA'], nADCNumChannels=2)

# test_cookbook_createHeaderPages(os.path.join(folder_dir, abf_f))

def abf_info(abf):
    print(abf)
    print('-'*40)
    print('ADC names and units')
    print(abf.adcNames)
    print(abf.adcUnits)
    print('Channel count and list')
    print(abf.channelCount)
    print(abf.channelList)
    print('data Byte start')
    print(abf.dataByteStart)
    # print(abf.headerText) -- way too much info! 

abf = pyabf.ABF(os.path.join(PATH_DATA, abf_f))
abf_info(abf)

print('Check headers of example data! -------')
for fex in ['171117_HFMixFRET.abf', '18425108.abf ', '180415_aaron_temp.abf', '17o05028_ic_steps.abf']:
    abf_ex = pyabf.ABF(os.path.join(PATH_DATA, fex))
    print('-'*80)
    abf_info(abf_ex)