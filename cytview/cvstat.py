from cgi import test
import matplotlib.pylab as plt
import numpy as np
import scipy.stats as scipy
import warnings

def significance(p):
    
   if (p < 0.0001): return("****")
   elif(p < 0.001): return("***")
   elif (p < 0.01): return("**")
   elif (p < 0.05): return("*")
   elif (p > 0.05): return("ns")
   else: return("")


def draw_lines(pval_list, compare, groupings, summary):
    # padding counter to prevent overlap of connecting lines
    pad_counter = np.full(shape=len(groupings), fill_value =0)
    
    n = 0
    while n < len(compare):
        
        comparison = compare[n]        
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
        plt.text(text_coord, linemax, significance(pval_list[n]), ha="center", fontsize=20)

        # add to padding counters
        pad_counter[comparison[0]] = pad_counter[comparison[0]] + 1
        pad_counter[comparison[1]] = pad_counter[comparison[1]] + 1

        n = n + 1


def multi_comparison(dataframe, compare, groupings, labels, summary, draw):
    
    perform_stats = True
    pval_list = []
    n = 0
    
    while n < len(compare):
         
        comparison = compare[n]
        control_means =  np.mean(dataframe.loc[:,groupings[comparison[0]]])
        test_means = np.mean(dataframe.loc[:,groupings[comparison[1]]])
           
        if len(control_means) < 2 or len(test_means) < 2:
            
            warning_msg = "2 or more observations per sample (n) are required to perform statistics between: " + \
            labels[comparison[0]] + " and " + labels[comparison[1]]
            
            warnings.warn(str(warning_msg))
            perform_stats = False
            break
        
        p_value = scipy.f_oneway(control_means, test_means)[1]
        pval_list.append(p_value)
        
        print(labels[comparison[0]], "vs", labels[comparison[1]], ": p value: ", str(round(p_value,6)), " (", significance(p_value), ")")
               
        n = n + 1
        
 
    if draw == True and perform_stats == True:
        draw_lines(pval_list, compare, groupings, summary)
