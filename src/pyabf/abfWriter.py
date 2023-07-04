"""
Code here relates to modification and de-novo creation of ABF files.
Files are saved as ABF1 format ABFs, which are easy to create because their
headers are simpler than ABF2 files. 

Many values (e.g., epoch waveform table) are left blank, so when they are read 
by an ABF reader their values may not make sense (especially when converted to 
floating-point numbers).

Lucas Koerner:
* modifications to support multiple channels with different names and units 2023/4/10
* modify so that FLOAT data format works 

"""

import struct
import numpy as np


def writeABF1(sweepData, filename, sampleRateHz, units='pA', 
              nADCNumChannels=1, FLOAT=False, names_input = [], DEBUG=False):
    """
    Create an ABF1 file from scratch and write it to disk.
    Files created with this function are compatible with MiniAnalysis.
    Data is expected to be a 2D numpy array (each row is a sweep).
    
    the sampleRateHz is assumed to be divided among all ADC channels
        so if sampling in parallel increase the sample rate by the number of channels
    
    """

    assert isinstance(sweepData, np.ndarray)

    # constants for ABF1 files
    BLOCKSIZE = 512
    HEADER_BLOCKS = 4

    # determine dimensions of data
    sweepCount = sweepData.shape[0]
    sweepPointCount = sweepData.shape[1]
    dataPointCount = sweepPointCount*sweepCount

    # predict how large our file must be and create a byte array of that size
    if FLOAT:
        bytesPerPoint = 4 # LJK
    else:
        bytesPerPoint = 2
    
    dataBlocks = int(dataPointCount * bytesPerPoint / BLOCKSIZE) + 1
    data = bytearray((dataBlocks + HEADER_BLOCKS) * BLOCKSIZE)

    # populate only the useful header data values
    struct.pack_into('4s', data, 0, b'ABF ')  # fFileSignature
    struct.pack_into('f', data, 4, 1.3)  # fFileVersionNumber
    struct.pack_into('h', data, 8, 5)  # nOperationMode (5 is episodic)
    struct.pack_into('i', data, 10, dataPointCount)  # lActualAcqLength
    struct.pack_into('i', data, 16, sweepCount)  # lActualEpisodes
    struct.pack_into('i', data, 40, HEADER_BLOCKS)  # lDataSectionPtr
    if FLOAT:
        struct.pack_into('h', data, 100, 1)  # nDataFormat is 1 for float32 -- not supported in pyABF and crashes clampFit
    else:
        struct.pack_into('h', data, 100, 0)  # nDataFormat is 1 for float32
    struct.pack_into('h', data, 120, nADCNumChannels)  # nADCNumChannels
    struct.pack_into('f', data, 122, 1e6 / sampleRateHz)  # fADCSampleInterval
    struct.pack_into('i', data, 138, sweepPointCount)  # lNumSamplesPerEpisode

    # These ADC adjustments are used for integer conversion. It's a good idea
    # to populate these with non-zero values even when using float32 notation
    # to avoid divide-by-zero errors when loading ABFs.

    fSignalGain = 1  # always 1
    fADCProgrammableGain = 1  # always 1
    lADCResolution = 2**15  # 16-bit signed = +/- 32768

    # determine the peak data deviation from zero
    maxVal = np.max(np.abs(sweepData))

    # set the scaling factor to be the biggest allowable to accommodate the data
    fInstrumentScaleFactor = 100
    for i in range(10):
        fInstrumentScaleFactor /= 10
        fADCRange = 10
        valueScale = lADCResolution / fADCRange * fInstrumentScaleFactor
        maxDeviationFromZero = 32767 / valueScale
        if (maxDeviationFromZero >= maxVal):
            break

    # prepare units as a space-padded 8-byte string
    # array up to 16 
    units = [units] if isinstance(units, str) else units 
    unitString = []
    names = []

    for i in range(16):
        try:
            unitString.append(units[i])
        except:
            unitString.append(units[-1]) # if units is not long enough use the last one 
        while len(unitString[i]) < 8: # pad with spaces 
            unitString[i] = unitString[i] + " "
        names.append(f'V{i}')
        try:
            names[i] = names_input[i]
        except: # name is not input
            pass
        while len(names[i])<10:
            names[i] = names[i] + " "

    if DEBUG:
        print(names)
        print(unitString)
    # store the scale data in the header
    struct.pack_into('i', data, 252, lADCResolution)
    struct.pack_into('f', data, 244, fADCRange)
    for i in range(16):
        if DEBUG:
            print(f'Unit string {unitString[i]} and name {names[i]}')
        struct.pack_into('f', data, 922+i*4, fInstrumentScaleFactor)
        struct.pack_into('f', data, 1050+i*4, fSignalGain)
        struct.pack_into('f', data, 730+i*4, fADCProgrammableGain)
        struct.pack_into('8s', data, 602+i*8, unitString[i].encode()) #sADCUnits
        struct.pack_into('10s', data, 442+i*10, names[i].encode()) #sADCChannelName
        # sampling sequence   # short is h 
        struct.pack_into('h', data, 378+i*2, i) #nADCPtoLChannelMap        # ADC PtoL physical to logical Map 
        if i < nADCNumChannels:
            struct.pack_into('h', data, 410+i*2, i) #nADCSamplingSeq
        else:
            struct.pack_into('h', data, 410+i*2, -1) #nADCSamplingSeq    
            
    # fill data portion with scaled data from signal
    dataByteOffset = BLOCKSIZE * HEADER_BLOCKS
    if DEBUG:
        print(f'databyteOffset {dataByteOffset}; greatest header offset {1050+i*15}')
    for sweepNumber, sweepSignal in enumerate(sweepData):
        sweepByteOffset = sweepNumber * sweepPointCount * bytesPerPoint
        for valueNumber, value in enumerate(sweepSignal):
            valueByteOffset = valueNumber * bytesPerPoint
            bytePosition = dataByteOffset + sweepByteOffset + valueByteOffset
            if FLOAT:
                struct.pack_into('f', data, bytePosition, value) # f is a 4 byte float -- LJK 
            else:
                struct.pack_into('h', data, bytePosition, int(value*valueScale)) # h is a short (2 byte integer)

    # save the byte array to disk
    with open(filename, 'wb') as f:
        f.write(data)
    return
