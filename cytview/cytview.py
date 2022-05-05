import seaborn as sns
import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import warnings

from cytview import cvstat

def point_plot(dataframe, measurment, identifier, groupings, labels, y_label=None, color='salmon', compare=None, figsize=None, draw=False):

    # generate a list of all values for each unique identifier
    combined_object = dataframe.groupby(identifier)[measurment].apply(list)
    
    # convert the set of lists to a dictionary and allow for unequal array lengths
    combined_object = pd.DataFrame({k: pd.Series(l) for k, l in combined_object.items()}).apply(pd.to_numeric)
    
    # cut off dataframe to 1000 sample observations to prevent computational strain
    combined_object = combined_object[0:1000] 
 
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
    figure = plt.figure(figsize=figsize)
    plt.ylabel(y_label, fontsize = 15)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        warnings.warn("UserWarning arose", UserWarning)
        sns.swarmplot(data=grouped_df, size=3, zorder=0.5, color=color)
    
    sns.boxplot(data=grouped_df, boxprops=dict(alpha=.5), whis=0.3,
                color="black", sym='')

    # collect boxplot details for statistical comparison and visualisation
    box_data = grouped_df.describe()
    
    if(compare==None):
        pass
    else:
        cvstat.multi_comparison(dataframe = combined_object, compare=compare, 
                                 groupings=groupings, labels=labels, box_data=box_data, draw=draw)
    
    control_line = np.median(grouped_df.iloc[:,0])
    plt.axhline(y=control_line, color='black', linestyle='--')
    plt.tight_layout()
    plt.show()





