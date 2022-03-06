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
import scipy.stats as s
import sys

pd.set_option("display.max_columns", None,'display.max_colwidth', -1)


all_data = pd.DataFrame()

def clean_df(df, keep, rename=None):
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
    if rename:
        newname = {k:r for k,r in zip(keep, rename)}
        df.rename(columns=newname,
                  inplace=True)
    return df


def hyp(x, y):
    return pd.DataFrame([math.sqrt(x**2+y**2) for x,y in zip(x,y)] )

def hyp(pos1, pos2): #pos1 and pos2 are zipped (x,y) tuples
    out = []
    for i in range(max(len(pos1), len(pos2))): # if you use pandas, they should be the same length, added max to throw error if your data is inconsistent
        out.append( math.sqrt((pos2[i][1]-pos1[i][1])**2 + (pos2[i][0]-pos1[i][0])**2) )
    return pd.DataFrame(out, columns=['hyp'])

for filename in sys.argv[1:]: # skip current filename

    #skip non csv files
    if not filename.endswith('csv'):
        continue
    df = pd.read_csv('data/'+filename)

    df = clean_df(df, ['timestamp', 'position_px_y-lightorange', 'position_px_x-lightorange', 'position_px_y-green', 'position_px_x-green', 'position_px_y-yellowneon', 'position_px_x-yellowneon'], ['t','oy','ox','gy','gx','yy','yx'])
    df.set_index('t', inplace=True)

    green = list(zip(df.gx,df.gy))
    yellow = list(zip(df.yx,df.yy))
    h = hyp(green, yellow)
    dist = h.hyp.mean()
    #dx = df.gx- df.yx
    #dy = df.gy- df.yy
    df.loc[:,"dx"] =df.gx- df.yx
    df.loc[:,"dy"] =df.gy- df.yy

    print(df.dx, df.dy)

    #print('shit\n' if len(df.dx) != len(h.hyp) else '', end='')
    angle = None
    if filename[0] == 's':
        tolerance = 3##################################### idk, pretty impossible to tell
        print(len(list(zip(h,df.dx,df.dy))))
        for h1,dx1,dy1 in zip(h.values.tolist(),df.dx.values.tolist(),df.dy.values.tolist()):#range(len(h.hyp)):
            h1 = h1[0]
            if h.hyp[h.first_valid_index()] - h1 > tolerance:
                print(h1,dx1,dy1)
                print(dx1,dy1)
                angle = math.atan(dy1/dx1)
                break
            else:
                pass#print(h.hyp[h.first_valid_index()] - h1) # tolerance

        print('angle',angle)
    print(filename)
    #print(np.mean(((df.gx- df.yx)**2+(df.gy- df.yy)**2)**.5)) # correct also
    #print('x,y', (x**2+y**2)**.5)

    print('dist', dist)# correct
    print('\n\n')

    #all_data["t_" + filename] = df["t"]
    #all_data.set_index('t', inplace=True)
    #row = pd.DataFrame({"angle":angle})
    #pd.concat(all_data, row)


#print(all_data)

all_data.to_csv("parsed_final_data.csv", index=False)

