
<img src="static/logo.png" />

### CytView is a python library which has been developed to handle high-throughout single cell imaging datasets generated from software such as CellProfiler. 


## API Reference

### Example: Input Matrix (first 5 rows)


| ImageNumber | ObjectNumber | Metadata_Well | Measurement_1 | Measurement_2 |
|-------------|--------------|---------------|---------------|---------------|
| 1           | 1            | A04           | 0.008474807   | 0.169154055   |
| 1           | 2            | A04           | 0.01052627    | 0.114010939   |
| 1           | 3            | A04           | 0.006294804   | 0.05234771    |
| 1           | 4            | A04           | 0.006413796   | 0.006516079   |
| 1           | 5            | A04           | 0.005213105   | 0.059943293   |


##  cytview.cell_plot()

```python
cytview.cell_plot(dataframe, measurment, identifier, obs_max = 500, color="Accent")
```

Randomly sample a subset of single-cell observations and plot cell-by-cell values CytView makes use of seaborn's swarmplot() and boxplot() functions and thus any plot-related parameters can be tweaked using matplotlib.

<img src="static/cell_plot.png" />


##  cytview.group_plot()
Sample single-cell observations and group samples by experimental replicates.ell-by-cell values CytView makes use of seaborn's swarmplot() and boxplot

```python
group_plot(dataframe, measurment, identifier, groupings, labels, obs_max = 500, color="Accent", compare=None, draw=False)
```
<img src="static/grouped_plot.png" width="300" />


```python
extract_values(dataframe, measurement, identifier, obs_max=500)
```

```python

           A04       A05       A06       C04       C05       C06       E04       E05       E06
2954  0.004288  0.003387  0.008706  0.008025  0.006866  0.006618  0.007125  0.005266  0.006731
2676  0.005719  0.004625  0.006905  0.005447  0.004007  0.005801  0.007522  0.004245  0.004388
1993  0.005470  0.007554  0.009259  0.003686  0.008447  0.005912  0.005385  0.005402  0.005988
2504  0.006326  0.006313  0.005011  0.005473  0.006047  0.005629  0.005572  0.006545  0.003686
487   0.006662  0.009883  0.006966  0.006744  0.006802  0.002728  0.006406  0.006283  0.005750
```

