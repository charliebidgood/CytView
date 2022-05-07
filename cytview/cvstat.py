import matplotlib.pylab as plt
import numpy as np
import scipy.stats as scipy

def significance(p):
    
   if (p < 0.0001): return("****")
   elif(p < 0.001): return("***")
   elif (p < 0.01): return("**")
   elif (p < 0.05): return("*")
   elif (p > 0.05): return("ns")
   else: return("")


def draw_lines(pval_list, compare, groupings, box_data):
    # padding counter to prevent overlap of connecting lines
    pad_counter = np.full(shape=len(groupings), fill_value =0)
    
    n = 0
    while n < len(compare):
        
        # pull boxplot data and esitamate the whisker length for both boxes
        b1_iqr = box_data.iloc[:,compare[n][0]]["75%"]
        b1_mean = box_data.iloc[:,compare[n][0]]["mean"]
        b1_whis = b1_iqr - b1_mean

        b2_iqr = box_data.iloc[:,compare[n][1]]["75%"]
        b2_mean = box_data.iloc[:,compare[n][1]]["mean"]
        b2_whis = b2_iqr - b2_mean

        # calculate y distances respective to the padding counter
        height_adjust = max(pad_counter[compare[n][0]:compare[n][1]+1])
        b1_ydist = b1_iqr + (b1_whis * (height_adjust+1)*2)
        b2_ydist = b2_iqr + (b2_whis * (height_adjust+1)*2)

        # draw connecting line
        linemax = max(b1_ydist, b2_ydist)

        plt.plot([compare[n][0],compare[n][1]], [linemax, linemax], color ="black")

        # calculate down line distances and shorten tem respective to padding counter
        b1_dist = ((linemax - (b1_iqr + 0.75*b1_whis))) / (pad_counter[compare[n][0]] + 1)
        b2_dist = ((linemax - (b2_iqr + 0.75*b2_whis))) / (pad_counter[compare[n][1]] + 1) 

        # draw down lines
        plt.plot([compare[n][0],compare[n][0]], [linemax, linemax - b1_dist], color ="black")
        plt.plot([compare[n][1],compare[n][1]], [linemax, linemax - b2_dist], color ="black")

        # show significance symbols
        text_coord = (compare[n][1] + compare[n][0]) / 2
        plt.text(text_coord, linemax, significance(pval_list[n]), ha="center", fontsize=20)

        # add to padding counters
        pad_counter[compare[n][0]] = pad_counter[compare[n][0]] + 1
        pad_counter[compare[n][1]] = pad_counter[compare[n][1]] + 1

        n = n + 1


def multi_comparison(dataframe, compare, groupings, labels, box_data, draw):
    
    print(box_data)
    
    pval_list = []
    
    n = 0
    while n < len(compare):

        control_means =  np.mean(dataframe.loc[:,groupings[compare[n][0]]])
        test_means = np.mean(dataframe.loc[:,groupings[compare[n][1]]])
        
        p_value = scipy.f_oneway(control_means, test_means)[1]
        pval_list.append(p_value)
        
        print(labels[compare[n][0]], "vs", labels[compare[n][1]], ": p value: ", str(round(p_value,6)))
               
        n = n + 1
        
    if draw:
        draw_lines(pval_list, compare, groupings, box_data)
        
