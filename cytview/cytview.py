import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings

warnings.simplefilter("ignore", UserWarning)
warnings.simplefilter("ignore", FutureWarning)

from cytview import cvstat

def extract_values(dataframe, measurement, identifier, obs_max=1000):
    
    # generate a list of all values for each unique identifier
    extracted_df = dataframe.groupby(identifier)[measurement].apply(list)
    # convert the set of lists to a dictionary and allow for unequal array lengths
    extracted_df = pd.DataFrame({k: pd.Series(l) for k, l in extracted_df.items()}).apply(pd.to_numeric)
    
    filtered_df = pd.DataFrame([])
    for column in extracted_df.columns:
        values = extracted_df[column][extracted_df[column].notnull()]
        if values.shape[0] < obs_max:
            filtered_df[column] = values.sample(n=values.shape[0], ignore_index=True)
        else:
            filtered_df[column] = values.sample(n=obs_max, ignore_index=True)
    return(filtered_df)


def cell_plot(dataframe, measurement, identifier, obs_max = 1000, 
              size=3, color="Accent", ax=None):
    
    extracted_df = extract_values(dataframe, measurement, identifier, obs_max)
    # swarmplot() will produce user errors if observations are falling outside the plot
    pal = sns.set_palette(sns.color_palette(color))

    sns.swarmplot(data=extracted_df, size=size, zorder=0.5,  palette=pal, 
                  edgecolor="gray", linewidth=0.25, ax=ax)

    sns.boxplot(data=extracted_df, boxprops=dict(alpha=.5), whis=0.3,
                color="black", showfliers=False, ax=ax)

    results = {"dataframe": extracted_df, "summary": extracted_df.describe()}
    return(results)


def group_plot(dataframe, measurement, identifier, groupings, labels, 
               obs_max = 1000, size=3, color="Accent", draw=False, ax=None):

    extracted_df = extract_values(dataframe, measurement, identifier, obs_max)
    
    # generate a dataframe containing the means of replicate samples
    grouped_df = pd.DataFrame([]) 
    means = pd.DataFrame([]) 

    # group replicate values together by adding their means into to grouped_df
    for x in groupings:
        values = extracted_df[x]
        means['mean'] = values.mean(axis=1)
        grouped_df = pd.concat([grouped_df, means['mean']], axis=1)
        
    for column in range(grouped_df.shape[1]):
        grouped_df.columns.values[column] = labels[column]
    
    # plotting functions
    plt.ylabel(measurement, fontsize = 15)
            
    pal = sns.set_palette(sns.color_palette(color))
    sns.swarmplot(data=grouped_df, size=size, zorder=0.5,  
                  palette=pal, edgecolor="gray", linewidth=0.25, ax=ax)
    
    sns.boxplot(data=grouped_df, boxprops=dict(alpha=.5), whis=0.3,
                color="black", showfliers=False, ax=ax)
    

    stats_table = cvstat.multi_comparison(dataframe = extracted_df, groupings=groupings,
                            labels=labels, summary=grouped_df.describe(), draw=draw)
           
    results = { "dataframe": grouped_df, "summary": grouped_df.describe(), "stats":stats_table}

    return(results)





