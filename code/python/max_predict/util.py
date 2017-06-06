# Utility functions to calculate simulation parameters
import sys
import math
import pandas as pd
import numpy as np
from scipy import signal as sig

C = 299792458 #speed of light m/s

# Int Hz
# float Radians per sec
# Converts prf and azimuthrate to pulses per angle in a scan cycle (360deg)
def pulsesperangle(prf, azimuthrate):
    anglepersec = math.degrees(azimuthrate)
    return prf/anglepersec


#shorthand for pulse per angle
def ppa(prf, azimuthrate):
    return pulsesperangle(prf,azimuthrate)


# Takes the desired angles per second and gives the radian counterpart
# useful for setting up simulator parameters
def getazimuthrate(degpersecond):
    return math.radians(degpersecond)


# Shorthand for getAzimuthrate
def getazr(degprsec):
    return getazimuthrate(degprsec)


# Max unambigous range given a pulse repetition frequency
def maxunambiguiousrange(prf):
    return C / (2 * prf)


# shorthand
def maxua(prf):
    return maxunambiguiousrange(prf)


# target: filename
# Start: int > 0
# end, step: positive int > 0
def maxua_graph(tar,start, end, step):
    original = sys.stdout
    sys.stdout = open(tar, 'w')
    print('prf max_unambiguous_range')
    for i in range(start, end, step):
        print('%i %f' %(i, maxua(i)))
    sys.stdout = original


# maxunamb: float range
# Window size in seconds
def windowsize(maxunamb):
    # R = v * t -> R/v = t
    mu = float(maxunamb)
    return mu/C


# Find peak indexes in sample
def analyze(seq, w):
    return sig.find_peaks_cwt(seq, np.arange(1,w))


def corr(seq):
    return sig.correlate(seq, np.ones(128)) / 128


def match(seq):
	mfilt=np.conjugate(seq)
	mfilt1=np.convolve(seq,mfilt,mode='full')
	return mfilt1
	
	
# Load csv sample file
def load(filename, colsToDrop = [0,2,3]):
    x = []
    df = pd.read_csv('%s'%(filename), header=None)
    df = df.drop(df.columns[colsToDrop],axis=1)
    df = df.values
    return np.array(df).flatten()
	
def save(filename, seq):
	np.savetxt(filename, seq, delimiter=",")