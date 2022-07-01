import seaborn as sns
import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import warnings

from cytview import cvstat

def extract_values(dataframe, measurement, identifier, obs_max=500):
    
    #generate a list of all values for each unique identifier
    extracted_df = dataframe.groupby(identifier)[measurement].apply(list)
    # convert the set of lists to a dictionary and allow for unequal array lengths
    extracted_df = pd.DataFrame({k: pd.Series(l) for k, l in extracted_df.items()}).apply(pd.to_numeric).dropna()
  
    extracted_df = extracted_df.sample(n=obs_max)
    return(extracted_df)


def cell_plot(dataframe, measurement, identifier, obs_max = 500, color="Accent"):
       
    extracted_df = extract_values(dataframe, measurement, identifier, obs_max)
      
    with warnings.catch_warnings():
        
        warnings.simplefilter("ignore")
        warnings.warn("UserWarning arose", UserWarning)
        
        pal = sns.set_palette(sns.color_palette(color))
        sns.swarmplot(data=extracted_df, size=3, zorder=0.5,  palette=pal)

    sns.boxplot(data=extracted_df, boxprops=dict(alpha=.5), whis=0.3,
                color="black", sym='')

    results = {"dataframe": extracted_df, "summary": extracted_df.describe()}
    return(results)



def group_plot(dataframe, measurement, identifier, groupings, labels, obs_max = 500, color="Accent", compare=None, draw=False):

    extracted_df = extract_values(dataframe, measurement, identifier, obs_max)
    
    # generate a dataframe containing the means of replicate samples
    grouped_df = pd.DataFrame([]) 
    means = pd.DataFrame([]) 

    for x in groupings:
        values = extracted_df[x]
        means['mean'] = values.mean(axis=1)
        grouped_df = pd.concat([grouped_df, means['mean']], axis=1)
        
    for column in range(grouped_df.shape[1]):
        grouped_df.columns.values[column] = labels[column]
    
    # plotting functions
    plt.ylabel(measurement, fontsize = 15)

    with warnings.catch_warnings():
         
        warnings.simplefilter("ignore")
        warnings.warn("UserWarning arose", UserWarning)
        
        pal = sns.set_palette(sns.color_palette(color))
        sns.swarmplot(data=grouped_df, size=3, zorder=0.5,  palette=pal)
    
    sns.boxplot(data=grouped_df, boxprops=dict(alpha=.5), whis=0.3,
                color="black", sym='')
  
    if(compare!=None):
        cvstat.multi_comparison(dataframe = extracted_df, compare=compare, groupings=groupings,
                                labels=labels, summary=grouped_df.describe(), draw=draw)
           
    results = { "dataframe": grouped_df, "summary": grouped_df.describe()}

    return(results)





