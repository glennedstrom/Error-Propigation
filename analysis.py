#TODO: 
#deliverables #4, excel
#
#
#
import pandas as pd
import matplotlib.pyplot as plt
import math
from errorProp import err
import numpy as np
import os
import sys


def clean_df(df, keep=None):
    if keep:
        for col in df.columns:
            if not col in keep:
                df.drop(col, axis=1, inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    df.dropna(axis=0, how='all', inplace=True)
    #remove error dots (adjust number if needed)
    for i in df:
        if df[i].count() < 20:
            df.drop(i, axis=1, inplace=True)
    return df

df = clean_df(pd.read_csv('data/measurements.csv'))


def hyp(pos1, pos2): #pos1 and pos2 are zipped (x,y) tuples
    out = []
    for i in range(max(len(pos1), len(pos2))): # if you use pandas, they should be the same length, added max to throw error if your data is inconsistent
        out.append( math.sqrt((pos2[i][1]-pos1[i][1])**2 + (pos2[i][0]-pos1[i][0])**2) )
    return pd.DataFrame(out, columns=['hyp'])


#zip (x,y) pairs
orange = list(zip(df['position_px_x-lightorange'], df['position_px_y-lightorange']))
pink = list(zip(df['position_px_x-hotpink'], df['position_px_y-hotpink']))

#get distance between two dots
dist = hyp(orange, pink)
dist.dropna(inplace=True)

avg_px = dist['hyp'].mean()

#1 px = 
px_to_m = .5/avg_px
print('one pixel is', px_to_m, 'meters')





df = pd.read_csv('parsed.csv')


for i in df:
    if not i[:5] == 'time_':
        #convert to meters
        df[i] = df[i].apply(lambda x: x*px_to_m)
        #make it become height
        df[i] = df[i].apply(lambda x: df[i].max() - x)

print(df)


df.to_csv("height_meters.csv", index=False)





#old method
"""def hyp(x,y):
    return math.sqrt((x[1]-x[0])**2 + (y[1]-y[0])**2)
distance__ = [hyp(x,y) for x,y in zip(zip(df['position_px_x-lightorange'],df['position_px_x-hotpink']), zip(df['position_px_y-lightorange'],df['position_px_y-hotpink']))]
"""



"""
#old lab
#print(df.info())
    df.drop(["frame_no", 'timestamp'], axis=1, inplace=True)
    ax = df.plot(x='position_px_x-green', y='position_px_y-green', label="Green", color='green')
    df.plot(x='position_px_x-hotpink', y='position_px_y-hotpink', label="Hot Pink", ax=ax, color='#FF69B4')
    df.plot(x='position_px_x-yellowneon', y='position_px_y-yellowneon', label="Neon", ax=ax, color='#FFF01F')
    ax.set_xlabel("x")
    ax.set_xlabel("y")
    plt.show()

    def hyp(x,y):
        return math.sqrt((x[1]-x[0])**2 + (y[1]-y[0])**2)

    width = [hyp(x,y) for x,y in zip(zip(df['position_px_x-green'],df['position_px_x-hotpink']), zip(df['position_px_y-green'],df['position_px_y-hotpink']))]

    length = [hyp(x,y) for x,y in zip(zip(df['position_px_x-yellowneon'],df['position_px_x-hotpink']), zip(df['position_px_y-yellowneon'],df['position_px_y-hotpink']))]

    unique = 0
    def area_err(w,l):
        if type(w) != float:
            print("aaaa")
        return w*l

    def std(data):
        average = sum(data)/len(data)
        s = sum([(i-average)**2 for i in data])
        return math.sqrt(s/(len(data)-1))

    def std_err(area):
        return std(area)/len(area)

    width = [i for i in width if not np.isnan(i)]
    length = [i for i in length if not np.isnan(i)]


    area = [area_err(w,l) for w,l in zip(width, length) if not np.isnan(w) and not np.isnan(l)]
    print("\nArea: statistical:",np.average(area), "±",std_err(area), "(%", std_err(area)/np.average(area)*100, ")")
    l = err(str(np.average(length)), float(std_err(length)))
    print("\nlength", l)
    w = err(str(np.average(width)), float(std_err(width)))
    print("\nwidth", w)

    print("Area (propigated): ", l*w)

#print(sum(area)/len(area))

#fig, axs = plt.subplots(1,2,sharey=True)


    plt.hist(width, bins=int(math.sqrt(len(width))), color="#24a600")
    plt.xlabel("Distance in Pixels", fontsize=16)
    plt.ylabel("Quantity", fontsize=16)
    plt.title("Histogram of Width", fontsize=20)
    plt.legend(["Pink dot to Green dot"])
    plt.show()

    plt.hist(length, bins=int(math.sqrt(len(length))), color="#d4d400")
    plt.xlabel("Distance in Pixels", fontsize=16)
    plt.ylabel("Quantity", fontsize=16)
    plt.title("Histogram of Length", fontsize=20)
    plt.legend(["Pink dot to Yellow dot"])
    plt.show()
"""
