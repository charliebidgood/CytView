import seaborn as sns
import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import warnings

from cytview import cvstat

def cell_plot(dataframe, measurment, identifier, obs_max = 1000, color="Accent"):
    
    dataframe = dataframe[0:obs_max]

    with warnings.catch_warnings():
        
        warnings.simplefilter("ignore")
        warnings.warn("UserWarning arose", UserWarning)
        
        pal = sns.set_palette(sns.color_palette(color))
        sns.swarmplot(data=dataframe, size=3, zorder=0.5,  palette=pal)

    sns.boxplot(data=dataframe, boxprops=dict(alpha=.5), whis=0.3,
                color="black", sym='')


def group_plot(dataframe, measurment, identifier, groupings, labels, obs_max = 1000, color="Accent", compare=None, figsize=None, draw=False):

    # generate a list of all values for each unique identifier
    combined_object = dataframe.groupby(identifier)[measurment].apply(list)
    
    # convert the set of lists to a dictionary and allow for unequal array lengths
    combined_object = pd.DataFrame({k: pd.Series(l) for k, l in combined_object.items()}).apply(pd.to_numeric)
    
    # cut off dataframe to 1000 sample observations to prevent computational strain
    combined_object = combined_object[0:obs_max] 
    
    # generate a dataframe containing the means of replicate samples
    grouped_df = pd.DataFrame([]) 
    means = pd.DataFrame([]) 

    for x in groupings:
        values = combined_object[x]
        means['mean'] = values.mean(axis=1)
        grouped_df = pd.concat([grouped_df, means['mean']], axis=1)
        
    for column in range(grouped_df.shape[1]):
        grouped_df.columns.values[column] = labels[column]
    
    # plotting functions
    plt.ylabel(measurment, fontsize = 15)

    with warnings.catch_warnings():
         
        warnings.simplefilter("ignore")
        warnings.warn("UserWarning arose", UserWarning)
        
        pal = sns.set_palette(sns.color_palette(color))
        sns.swarmplot(data=grouped_df, size=3, zorder=0.5,  palette=pal)
    
    sns.boxplot(data=grouped_df, boxprops=dict(alpha=.5), whis=0.3,
                color="black", sym='')

    # collect boxplot details for statistical comparison and visualisation
    summary = grouped_df.describe()
    
    if(compare!=None):
        cvstat.multi_comparison(dataframe = combined_object, compare=compare, 
                                 groupings=groupings, labels=labels, summary=summary, draw=draw)
           
    return(summary)





