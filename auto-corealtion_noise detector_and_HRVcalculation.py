# -*- coding: utf-8 -*-
"""
Created on Wed Mar4 10 13:50:30 2021

Collection of tools for HRV segmentation from ECG signal

@author: Devender
"""
import h5py
import numpy as np
import wfdb
import unisens
import datetime
import heartpy as hp
import pandas as pd
import scipy
import matplotlib.pyplot as plt
import neurokit2 as nk

# from .SignalTools import buffer1D, get_label, get_label_multiclass
from . import SignalTools
from sklearn.model_selection import GroupKFold
import os
from ecgdetectors import Detectors

detectors = Detectors(1024)


def \
        get_rpeak_labels(rpeaks, ecg_labels):
    return np.array(ecg_labels[rpeaks], dtype='int32')

def filter_rri(rri, rpeaks, t1=0.3, t2=2):
    """
    threshold 30 bpm and 200 bpm
    """
    print("*****rpeaks  in filter rri*****")
    print(rpeaks)
    print("*****rri in filter rri*****")
    print(rri)

    orignal_rri= rri
    orignal_rpeaks=rpeaks

    idx = [idx for idx, val in enumerate(rri) if val > t1 and val < t2]

    filtered_rri=rri[idx]
    filter_rpeaks=rpeaks[idx]

    return rri[idx], rpeaks[idx]

def get_rri(rpeaks, fs, filt=False):
    """ Extract RR intervals from rpeak locations and find the corresponding
    label to each RR interval.

    # Arguments
        rpeaks: numpy array, with sample index of each R peak in the
            corresponding ECG signal.
        ecg_labels: numpy array, binary label of each sample in the ECG
            signal.
        fs: float or int, sampling freaquency of ECG signal.
        filt: boolean, if filt is "True" the RRI is filtered resulting in
            rejecting physically impossible values (bpm > 200 or bpm < 30)

    # Outputs
        rri: numpy array, with RR intervals
        rri_labels: numpy array, with binary label of each RR interval.
        rpeaks: numpy array, with sample index of each R peak in the
            corresponding ECG signal.
    """

    rri = np.true_divide(np.diff(rpeaks), fs)
    # rri_labels = get_rpeak_labels(rpeaks, ecg_labels)[1:]

    rpeaks = rpeaks[1:]

    if filt:
         rri,rpeaks = filter_rri(rri, rpeaks)

    return rri, rpeaks


def signalQualityForRRCalculation(signal):
    fs = 1024  # Sampling rate (512 Hz)
    data = signal  # 2 sec of data b/w 0.0-100.0

    #Check if signal is not empty
    if (len(data) < 8 * fs):
           return 'bad'

    # Get real amplitudes of FFT (only in postive frequencies)i
    fft_vals = np.absolute(np.fft.rfft(data))

    # Get frequencies for amplitudes in Hz
    fft_freq = np.fft.rfftfreq(len(data), 1.0 / fs)

    # Define EEG bands
    eeg_bands = {'ecg': (.67, 50),
                 #                  'hf_noise': (50, 100),
                 #                  'lf_noise': (0, .5),
                 }

    # Take the mean of the fft amplitude for each EEG band
    eeg_band_fft = dict()
    for band in eeg_bands:
        freq_ix = np.where((fft_freq >= eeg_bands[band][0]) &
                           (fft_freq <= eeg_bands[band][1]))[0]
        eeg_band_fft[band] = np.mean(fft_vals[freq_ix])

    # Logice for rejecting noise
    # if(eeg_band_fft)

    if ((eeg_band_fft['ecg'] < .001) or (eeg_band_fft['ecg'] > .400)):

        #print("Bad_fft-- " + str(eeg_band_fft) + " correlation mean " + str(corelation(signal)))

        return 'bad'
    else:

        if (corelation(signal) > 300 or corelation(signal) == 'nan'):
            #print("Good_fft-- " + str(eeg_band_fft), " correlation mean " + str(corelation(signal)))

            return 'good'
        else:
            #print("bad_fft-due to correlation-- " + str(eeg_band_fft), " correlation mean " + str(corelation(signal)))

            return 'bad'

def corelation(signal):
    a = scipy.signal.correlate(signal, signal)
    peaks, _ = scipy.signal.find_peaks(a, )
    if (len(peaks) > 450):
        #print("number of peaks>500 " + str(len(peaks)))
        return 0
    peak_values = a[peaks]
    peaks = peaks[np.argsort(peak_values)][::-1][0:11]

    #print(peaks.size)

    if (0 < peaks.size < 9):
        #print("returned 1000  as peask are <10")
        return 1000

    # sorting of peaks from hight to lowest
    # peaks, _ = find_peaks(x, distance=150)

    # plt.plot(a)
    # plt.plot(peaks[0:11], a[peaks[0:11]], "x")
    # plt.show()
    # Mean
    #print("Mean " + str(np.mean(np.abs(np.diff(peaks[0:11])))))
    return np.mean(np.abs(np.diff(peaks[0:11])))


def create_hrv_data_for_unisens(read_input_unisens_file, out_dir, wL, oL, multiclass=False):
    path= read_input_unisens_file
    u = unisens.Unisens(read_input_unisens_file)
    #/Users/deku/PycharmProjects/AF/u1t2m3@cachet.dk/


    wL=30

    fs = 1024

    #intersting usecase arround 3600 to 3640
    start_time=0
    end_time= int( float(u.duration))
    #end_time =10000
    signal = u['ecg.bin']
    data = signal.get_data()
    data = data[0]
    #Bandpass Filter for removing Noise
    bandpass_signal = hp.filter_signal(data, cutoff=[.67, 50], sample_rate=1024, order=3, filtertype='bandpass')
    filtered_signal = hp.smooth_signal(bandpass_signal, sample_rate=1024, polyorder=6)

    print("calculating r peaks "+str(datetime.datetime.now()))

    f2 = h5py.File(out_dir, 'w')
    X = np.empty((0, wL))
    SAMPLE_IDX = np.empty((0, wL))
    r_peaks_full=np.empty(0,dtype=int)

    if os.path.exists(path + "/" + "noise.csv"):
        os.remove(path + "/" + "noise.csv")
        print("Deleted old noise.csv file")
    else:
        print('File  noise.CSV does not exists')

    with open(path + "/" + "noise.csv", 'a') as f:

        w = 10
        counter = 0

        for i in range(start_time, end_time, w):
            print(str(i) + "==" + str(i + w))
            start = i
            if i + w < end_time:
                end = i + w
            else:
                end = end_time

            # _, nk_rpeaks = nk.ecg_peaks(filtered_signal[0:end * fs], sampling_rate=1024)
            if signalQualityForRRCalculation(filtered_signal[fs * start:fs * end]) == 'good':
                rpeaks_list = detectors.pan_tompkins_detector(filtered_signal[fs * start:fs * end])
                rpeaks = np.asarray(rpeaks_list)
                rpeaks = rpeaks + (counter * w * fs)
                counter = counter + 1
                r_peaks_full = np.concatenate((r_peaks_full, rpeaks), axis=0)
            else:
                counter = counter + 1
                inset_offset_indexs = pd.DataFrame([[start*fs, end*fs, "noise"]],
                                                   columns=['start', 'end',"true_label"])
                inset_offset_indexs.to_csv(f, header=f.tell() == 0, index=False)

            # rpeaks = nk_rpeaks['ECG_R_Peaks'][:]

            #print("Number of R peaks= " + str(len(r_peaks_full)))
            #print(" r peak calculation done " + str(datetime.datetime.now()))

            # ecg_labels= np.array()
            # calculate RR intervals

    f.close

    print("calculating rri starts " + str(datetime.datetime.now()))
    RRI, rpeaks = get_rri(rpeaks=r_peaks_full, fs=fs, filt=True)
    print("rri calculation done ")

    print("*****iafter get RRI *****" + str(datetime.datetime.now()))

    #print(RRI)
    #print(rpeaks)

    #print(RRI.shape)
    #print(rpeaks.shape)

    # windowing

    if(len(RRI)!=0):
     RRI = SignalTools.buffer1D(RRI, wL, oL)
     rpeaks = SignalTools.buffer1D(rpeaks, wL, oL)
     print("******after windowing****" + str(datetime.datetime.now()))

     print(RRI.shape)
     print(rpeaks.shape)

     X = np.concatenate((X, RRI), axis=0)
     SAMPLE_IDX = np.concatenate((SAMPLE_IDX, rpeaks), axis=0)


    # Update




    """ Creates HRV data set

    """
    """wL: integer, window length in samples
        oL: integer, number of overlapping samples in each window"""

    print("before Data saving in file")
    print(X)
    print("before index saving in file")
    print(SAMPLE_IDX)
    f2['Data'] = X.reshape((len(X), wL, 1))
    f2['Sample_idx'] = SAMPLE_IDX
    # f2['Labels'] = LABELS
    # f2['Groups'] = GROUPS
    f2['Signal']= filtered_signal[fs*start_time:fs*end_time]
    f2['r_peaks']=r_peaks_full

    f2.close()
    print("******Finished****" + str(datetime.datetime.now()))