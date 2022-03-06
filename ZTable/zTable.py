# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Glenn Edstrom
# Section:      575
# Assignment:   Lab HW5-ConfidenceInterval
# Date:         21 2 22
#

import csv
import matplotlib.pyplot as plt
import numpy as np
import statistics as s
import scipy.stats as stats
import math


#Part 1 a
with open('CIData.txt') as csv_file:

    sample = [float(i.strip()) for i in csv_file.readlines()]

def calculate(data):


# Statistics:
    temps_labels = ["Mean","Mode","Median","Variance","Std Deviation"]

    temps = []

    temps.append(s.mean(data))
    temps.append(s.mode(data))
    temps.append(s.median(data))
    temps.append(s.variance(data))
    temps.append(s.stdev(data))

    return {key:value for key, value in zip(temps_labels, temps)}


def print_data(data):

    for key, val in data.items():
        print('{:25s} {:>10.2f}'.format(key, val))
    print("\n")





#Part 1
std = 2.65 # lbs/ft**3
stdx = std/math.sqrt(len(sample))
conf = .8
savg = s.mean(sample)

z = (-savg)/stdx

print(std, stdx, savg)


"""
print("1. b")
print("Temperature data:")
tempdata = calculate(temp)
print_data(tempdata)


#Part 1 c
print("1. c")
print("Age data:")
ageData = calculate(age)
print_data(ageData)

#Part D graphs


# Temperature Histogram:
plt.hist(x=temp, bins=int(math.sqrt(len(temp))))
plt.xlabel('Temperatures')
plt.ylabel('Frequency')
plt.title('Temperatures Histogram')
plt.savefig('temperature_histogram.png')
plt.show()

#Part 2

m = 100
std = 5

# Calculating probability of an event 𝑃(16 ≤ x ≤ 19.99):
x = 140

z = (x - m)/std

P = 1 - stats.norm.cdf(z)

print('2. IQ of 140 or greater: P('+str(x)+' ≤ x ) = {:.3e} %'.format(P*100), sep='')



#Part 3

def binary_search(m, std, target, rng=None):
    if not rng:# initialize the bounds of the search
        limit = m
        if stats.norm.cdf((limit - m)/std) > target:# may break if target == .5
            while stats.norm.cdf((limit - m)/std) > target:
                limit -= std
        else:
            while stats.norm.cdf((limit - m)/std) < target:
                limit += std
        rng = [min(limit, m), max(limit, m)]

    guess = (rng[0] + rng[1])/2
    ans = stats.norm.cdf((guess - m)/std)

    #exit condition
    if ans//1e-15 == target//1e-15:#decimal places accuracy
        return guess

    if ans > target:#shrink
        return binary_search(m, std, target, rng=[rng[0], guess])

    else:#grow
        return binary_search(m, std, target, rng=[guess,rng[1]])

m = 10
std = 2

warrenty_years = binary_search(m, std, .05)

print("3. Maximum warrenty length in years:", warrenty_years)

#Part 4

# 2 std's away from the mean positive direction

m = 6
std = 1

x = 8

z = (x - m)/std

P = 1 - stats.norm.cdf(z)

print('4. Chance your hot chocolate cup will overflow: P('+str(x)+' ≤ x ) = {:.4f} %'.format(P*100), sep='')

#Part 5

m = 8000
std = 200

warrenty_years = binary_search(m, std, .02)

print("5. Maximum lightbulb warrenty in hours:", warrenty_years)
"""
