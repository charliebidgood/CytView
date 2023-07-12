import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as scipy
import warnings
import pandas as pd

def significance(p):
    
   if (p < 0.0001): return("****")
   elif(p < 0.001): return("***")
   elif (p < 0.01): return("**")
   elif (p < 0.05): return("*")
   elif (p > 0.05): return("ns")
   else: return("")


def draw_lines(pval_list, groupings, summary):
    # padding counter to prevent overlap of connecting lines
    pad_counter = np.full(shape=len(groupings), fill_value =0)
        
    for idx, pvalue in enumerate(pval_list):
        
        comparison = [0,idx+1]       
        # pull boxplot data and esitamate the whisker length for both boxes
        b1_iqr = summary.iloc[:,comparison[0]]["75%"]
        b1_mean = summary.iloc[:,comparison[0]]["mean"]
        b1_whis = b1_iqr - b1_mean

        b2_iqr = summary.iloc[:,comparison[1]]["75%"]
        b2_mean = summary.iloc[:,comparison[1]]["mean"]
        b2_whis = b2_iqr - b2_mean

        # calculate y distances respective to the padding counter
        height_adjust = max(pad_counter[comparison[0]:comparison[1]+1])
        b1_ydist = b1_iqr + (b1_whis * (height_adjust+1)*2)
        b2_ydist = b2_iqr + (b2_whis * (height_adjust+1)*2)

        # draw connecting line
        linemax = max(b1_ydist, b2_ydist)

        plt.plot([comparison[0],comparison[1]], [linemax, linemax], color ="black")

        # calculate down line distances and shorten tem respective to padding counter
        b1_dist = ((linemax - (b1_iqr + 0.75*b1_whis))) / (pad_counter[comparison[0]] + 1)
        b2_dist = ((linemax - (b2_iqr + 0.75*b2_whis))) / (pad_counter[comparison[1]] + 1) 

        # draw down lines
        plt.plot([comparison[0],comparison[0]], [linemax, linemax - b1_dist], color ="black")
        plt.plot([comparison[1],comparison[1]], [linemax, linemax - b2_dist], color ="black")

        # show significance symbols
        text_coord = (comparison[1] + comparison[0]) / 2
        plt.text(text_coord, linemax, significance(pval_list[idx]), ha="center", fontsize=20)

        # add to padding counters
        pad_counter[comparison[0]] = pad_counter[comparison[0]] + 1
        pad_counter[comparison[1]] = pad_counter[comparison[1]] + 1

 

def multi_comparison(dataframe, groupings, labels, summary, draw):
    
    perform_stats = True
    control = dataframe[groupings[0]].mean(axis=1)
    
    tests = []
    for idx, test in enumerate(groupings[1:]):
        tests.append(dataframe[test].mean(axis=1).values)
   
    pval_list = scipy.dunnett(*tests, control=control).pvalue

    for idx, pvalue in enumerate(pval_list):
        
        stars = significance(pvalue)
        pval_notation = str('{:.2e}'.format(pvalue))

        print(f"{labels[0]} vs {labels[idx+1]} : p value: {pval_notation} ({stars})")
           
    if draw == True and perform_stats == True:
        draw_lines(pval_list, groupings, summary)
