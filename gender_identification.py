#!/usr/bin/env python
# -*- coding: cp1250 -*-


from __future__ import division
from os import listdir
from os.path import isfile, join, splitext
from matplotlib.pyplot import xscale
from scipy import fft
from scipy.io.wavfile import read
from pylab import plot, xlabel, ylabel, savefig
from numpy import linspace, mean
from scikits.audiolab import wavread
import sys

__author__ = 'inf106637'


# GLOBAL CONST HERE:
samplingRate = 44100    # as name of var
mypath = "train"        # path to wav files in the project folder


# list with all files in the directory described above
def load_all_files(_path):
    print "\n============================================="
    print "=> Trying to load all 'wav' files..."
    # all_files = os.listdir("train")
    all_files = [f for f in listdir(_path) if isfile(join(_path, f))
                 and splitext(f)[1] == ".wav"]
    __samples = []
    male_filecount = 0
    female_filecount = 0
    for f in all_files:
        p = _path + "/" + f
        sys.stdout.write('... ' + f)
        data, rate, encoding = wavread(p)
        sig = [mean(d) for d in data]
        __samples.append({'name': f, 'gender': f[-5:-4], 'signal': sig, 'sample_rate': rate})
        if f[-5:-4] == "M":
            male_filecount += 1
        else:
            female_filecount += 1
        print '   ...loaded!'

    __counters = {"male_count": male_filecount, "female_count": female_filecount}
    return __samples, __counters
    print "=> All files loaded succesfully!..."
    print "============================================="
    # print str(len(data)) + " __samples"
    # samplerate = data[0].split()[3]
    # print samplerate + "Hz"
    # # else: => " + str(1 / float(samplerate)) + " seconds per sample"
    # print str(len(data) / float(samplerate)) + "s"
    # lengthins = len(data) / float(samplerate)


# tries to recognize gender from sample wav file
def recognize_gender(_sample):
    print "\n=> Trying to recognize gender from sample: ", _sample
    t = 3
    w = _sample['sample_rate']
    n = w * t
    signal = _sample['signal']
    nframe = len(signal)

    if n > nframe:
        n = nframe
    frequency = linspace(0, w, n, endpoint=False)
    spectrum = fft(signal[0:n])
    spectrum = abs(spectrum)
    freq, amp = [], []

    for i in range(len(frequency)):
        if 85 < frequency[i] < 255:
            freq.append(frequency[i])
            amp.append(spectrum[i])
    index = amp.index(max(amp))
    avg_freq = freq[index]

    if avg_freq < 175:  # avg_freq_M <0-175)
        return 'M'
    else:               # avg_freq_K <175-...)
        return 'K'


# all procedures doing the %-tage counting and printing on STDOUT
def do_algo(_samples, counters):
    # few "global method" vars...
    shot_males = 0
    shot_females = 0
    shot_correct = 0
    # starting the work to be done...
    print "\n============================================="
    print "=> Starting the main algorithm..."
    for sample in _samples:
        gender = recognize_gender(sample)  # call for another of MY functions, one ABOVE^

        if gender == sample['gender']:
            shot_correct += 1

            if gender == "M":
                shot_males += 1
            if gender == "K":
                shot_females += 1
            else:
                print "\n=> algorithm returned = ", sample['name']

            print "...", sample['name'], "...correct!"
        else:
            print "...", sample['name'], "... not good, sry :<"

    all_count = counters['male_count'] + counters['female_count']
    print "\n=> Stats:"
    print "good shots for males: ", shot_males, "/", counters['male_count']
    print "good shots for females: ", shot_females, "/", counters['female_count']
    print "together: ", shot_correct, "/", all_count, " (", shot_correct / all_count * 100, "%)"
    print "============================================="


# make plots from given samples - NOT USED IN PROGRAMME
def make_plots(_samples):
    print "\n============================================="
    print "=> starting all the plotting..."
    for sample in _samples:
        print "plotting file: " + sample['name']
        w = sample['sample_rate']
        T = 20

        n = len(sample['signal'])

        signal = sample['signal'][0:n]             # funkcja spróbkowana

        print "=> counting 'fft method' on samples..."
        signal_ = fft(signal)
        signal_ = abs(signal_)

        print "=> plotting samples..."
        freqs = linspace(0, w, n, endpoint=False)
        plot(freqs[:int(len(freqs)/2)], signal_[:int(len(freqs)/2)], '-')
        xlabel("sample rate")
        ylabel("sample count / constans")
        xscale('linear', rotation=45)

        print "=> saving plots in pdf files..."
        savefig("plots/" + sample['nazwa'] + ".pdf")
    print "=> DONE!...."
    print "============================================="



# MAIN FUNCTION OF PROGRAMME
if __name__ == '__main__':
    samples, counters = load_all_files(mypath)  # wczytanie plikow
    print counters                              # print wyniki
    do_algo(samples, counters)                  # poka wykresy