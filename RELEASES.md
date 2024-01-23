# Release History


## Version 1.1.1
* Added the ability to change size of points within cell_plot() and group_plot()
* Removed drawing of the statistical comparison lines, too difficult to control for 
* Downsampling now ignores NaN values and variable sample sizes are now allowed. This prevents groups with low sample sizes (n) affecting the rest of the dataset. 
* Statistical values are now exported as a pandas dataframe with rather than printed.


## Version 1.1.0
* Integrated Dunnett's multiple comparison test using SciPy 1.11's recently added function: [scipy.stats.dunnett()](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.dunnett.html).
* Significance and P Values are now only generated between the first sample (control) and subsequent samples. Future revisions will add more comparison flexibility.
* Added minimum versions for package dependencies in requirements.txt and setup.py.
* Minor fixes which prevented more recent versions of numpy being unable to compute means on pandas dataframe.  
* Updated example notebook to showcase new changes.

## Version 1.0.0
Initial Release of CytView
