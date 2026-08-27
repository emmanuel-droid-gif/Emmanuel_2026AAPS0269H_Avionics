import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

#Reading the data provided in the csv file and saving it in a variable
depth = pd.read_csv(r'C:\Everything important\VSS codes\Seds Entry projects\Odyssey finding the seafloor\DepthData.csv')

#Converting all the values to the numerical type so tht incase of any NULL values they get converted to NaN which can be dealt with later
depth['Depth (m)'] = pd.to_numeric(depth['Depth (m)'], errors = "coerce")  

#Converting a column into an array to plot it later(We use copy = True to ensure tht when we make changes to the given values if necessary then the originial copy is not affected)
time_array = depth['Point'].to_numpy(copy=True)
depth_array = depth['Depth (m)'].to_numpy(copy=True)

#Obtaining the mean and std values for later use in error correcting
diffs = np.diff(depth_array)
mean = np.nanmean(np.abs(diffs))
std_dev = np.nanstd(np.abs(diffs))

# Editing the provided csv depth data to remove and edit erratic values
for i in range(len(diffs)-1):
    if diffs[i] > 0:
        if diffs[i+1] < 0:
            if diffs[i] > mean + 1.5*std_dev:
                depth_array[i+1] = (depth_array[i] + depth_array[i+2])/2
    elif diffs[i] < 0:
        if diffs[i+1] > 0:
            if (diffs[i])*(-1) > mean + 1.5*std_dev:
                depth_array[i+1] = (depth_array[i] + depth_array[i+2])/2     
    elif np.isnan(diffs[i]):
        if np.isnan(depth_array[i]):
            continue
        else:
            depth_array[i+1] = (depth_array[i] + depth_array[i+2])/2


#Plotting and showing the graph, Animating the plotting of each point 

fig, ax = plt.subplots()
line, = ax.plot([], [])

ax.set_xlim(time_array.min(), time_array.max())
ax.set_ylim(time_array.min(), time_array.max())
ax.set_xlabel("Time (s)")
ax.set_ylabel("Depth (m)")
ax.set_title("Ship Depth Over Time")
ax.invert_yaxis()   # optional, if you want deeper = lower on screen

def update(frame):
    line.set_data(time_array[:frame+1], depth_array[:frame+1])
    return line,

ani = FuncAnimation(fig, update, frames=len(time_array), interval=1000)

plt.show()
