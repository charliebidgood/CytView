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


def draw_stars(pval_list, groupings, summary):
    # padding counter to prevent overlap of connecting lines    
    for idx, pvalue in enumerate(pval_list):
        upper_quartile = summary.iloc[:,idx+1]["75%"]
        mean_value = summary.iloc[:,idx+1]["mean"]
        y_star = (upper_quartile - mean_value) + upper_quartile
        x_star = idx+1
        plt.text(x_star, y_star, significance(pval_list[idx]), ha="center", fontsize=10)

def multi_comparison(dataframe, groupings, labels, summary, draw):
    control = dataframe[groupings[0]].mean(axis=1).dropna()
    tests = []

    for idx, test in enumerate(groupings[1:]):
        tests.append(dataframe[test].mean(axis=1).dropna().values)
   
    pval_list = scipy.dunnett(*tests, control=control).pvalue
    stats_table = pd.DataFrame({
            "comparison": [],
            "p_value": [],
            "significance": []})
   
    for idx, pvalue in enumerate(pval_list):
        stars = significance(pvalue)     
        entry =pd.DataFrame({"comparison": [f"{labels[0]} vs {labels[idx+1]}"],
                             "p_value": [pvalue],
                             "significance": [stars]})

        stats_table = pd.concat([stats_table, entry])
                   
    if draw == True:
        draw_stars(pval_list, groupings, summary)
    return (stats_table)