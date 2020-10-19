# Map of the Universe 2018

### 3D Map of the Universe - Instructions 
#### By Amena Faruqi (Undergraduate Research Opportunities Programme at Imperial College London)


3D_MoU -> plots the entirety of any database(s) given, for larger/many databases this may take some time.

3D_MoU_subset -> plots the entirety of any "small" databases given, for larger databases selects a random subset of datapoints to plot. The definition of "small" can be altered at the start of the 'plot_data' function, it is currently set to databases with fewer than 800 entries.

To run either of the above:
1. Place all databases to be plotted in the `data` directory. Databases MUST be in CSV format and contain the following fields, filled in: ra, dec, dist, date, type.
2. Run, a window containing the 3D plot should open within about 30s.

- Left-click and drag to rotate the plot
- Right-click and drag up or down to zoom in or out
- Move the slider at the bottom of the plot to view the year by which the plotted objects had been discovered. Note that the slider/plot may take a few seconds to update, especially when larger datasets are being plotted. Slider ranges from 1700 to 2018.  

------------------------------------------------------------------------------------------------------------------------------------------------------------ 

3D_MoU_gifmaker -> produces a gif showing the varition of the MoU over time, of which the timesteps can be adjusted. 

To run:
1. Place all databases to be plotted in the same directory as the python file. 
2. Run, the gif should be produced within a few minutes in the same directory. 
