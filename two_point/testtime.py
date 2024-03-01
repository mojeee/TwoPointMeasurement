import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the CSV file
path = "C:/Users/ghaza/OneDrive/Desktop/thesis/repo/M1E_tran_VDD_1,0V.DAT"
df = pd.read_csv(path, sep='\t', decimal=',', thousands=None, engine='python')

# Replace commas with dots and update scientific notation
df = df.applymap(lambda x: x.replace(',', '.').replace('E', 'e') if isinstance(x, str) else x)
df = df.apply(pd.to_numeric, errors='coerce')

# Rename the columns to lowercase
df.columns = ['Time', 'vin1', 'vout']



# Find min and max values
vout_min = df['vout'].min()
vout_max = df['vout'].max()

# Define smaller thresholds
threshold_min = 0.15 * (vout_max - vout_min)
threshold_max = 0.15 * (vout_max - vout_min)

# Filter data within a threshold around min and max values
vout_within_min_threshold = df[(df['vout'] >= vout_min) & (df['vout'] <= vout_min + threshold_min)]
vout_within_max_threshold = df[(df['vout'] >= vout_max - threshold_max) & (df['vout'] <= vout_max)]
print("Data within Min Threshold:")
print (vout_within_min_threshold)

# Plot vout against time
plt.figure(figsize=(10, 6))

# Plot raw data line
plt.plot(df['Time'], df['vout'], color='gray', label='Raw Data')

# Mark individual points for different segments based on thresholding
plt.scatter(vout_within_min_threshold['Time'], vout_within_min_threshold['vout'], color='red', label='Within Min Threshold', marker='o')
plt.scatter(vout_within_max_threshold['Time'], vout_within_max_threshold['vout'], color='green', label='Within Max Threshold', marker='o')


# Sort the DataFrame by the 'Time' column

def find_gap_indices(df, threshold:float = 0.1):
    # Sort the DataFrame by the 'Time' column
    df_sorted = df.sort_values(by='Time')
    # Calculate the difference between consecutive time values
    time_diff = df_sorted['Time'].diff()
    # Find the index where the gap occurs (difference is larger than a threshold)
    gap_indices = time_diff[time_diff > threshold].index
    gap_times = df_sorted.loc[gap_indices, 'Time']
    return gap_indices, gap_times

gap_indices_min, gap_times_min = find_gap_indices(vout_within_min_threshold)
gap_indices_max, gap_times_max = find_gap_indices(vout_within_max_threshold)


print("Gap indices:", gap_indices_min)
print("Time values at the gaps:", gap_times_min)
print("Gap indices:", gap_indices_max)
print("Time values at the gaps:", gap_times_max)
min_second_gap_time = gap_times_min.iloc[1]
print("Second min gap time:", min_second_gap_time)
max_second_gap_time = gap_times_max.iloc[1]
print("Second max gap time:", max_second_gap_time)
selected_min_data = vout_within_min_threshold[(vout_within_min_threshold['Time'] < gap_times_min.iloc[2]) & (vout_within_min_threshold['Time'] > gap_times_min.iloc[1])]
print("Selected min data:", selected_min_data)
min_avg = selected_min_data['vout'].mean()
print("Min average:", min_avg)
selected_max_data = vout_within_max_threshold[(vout_within_max_threshold['Time'] < gap_times_max.iloc[2]) & (vout_within_max_threshold['Time'] > gap_times_max.iloc[1])]
print("Selected max data:", selected_max_data)
max_avg = selected_max_data['vout'].mean()
print("Max average:", max_avg)
total_avg = (min_avg + max_avg) / 2
print("Total average:", total_avg)
# Plot the rest with different color
other_indices = df.index.difference(vout_within_min_threshold.index.union(vout_within_max_threshold.index))
print("Other indices:", df.loc[other_indices])
other_indices_data = df.loc[other_indices]
print("Other indices data:", other_indices_data['Time'])
# print th other indices time is between the second min gap time and the second max gap time
selected_points = other_indices_data[(other_indices_data['Time'] > min_second_gap_time) & (other_indices_data['Time'] < max_second_gap_time)]
if selected_points.empty:
    selected_points = other_indices_data[(other_indices_data['Time'] < min_second_gap_time) & (other_indices_data['Time'] > max_second_gap_time)]
print("Selected points:", selected_points)
# fit a line to the vout values of the selected points and save parameters for further use
# y = mx + c
# m = (nΣxy - ΣxΣy) / (nΣx^2 - (Σx)^2)
# c = (Σy - mΣx) / n
n = len(selected_points)
x = selected_points['Time']
y = selected_points['vout']
m = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (n * np.sum(x ** 2) - (np.sum(x)) ** 2)
c = (np.sum(y) - m * np.sum(x)) / n
# find the time value at the total_avg time
total_avg_time = (total_avg - c) / m
print("Total average time:", total_avg_time)






min_second_gap_time = gap_times_min.iloc[2]
print("Second min gap time:", min_second_gap_time)
max_second_gap_time = gap_times_max.iloc[2]
print("Second max gap time:", max_second_gap_time)
selected_min_data = vout_within_min_threshold[(vout_within_min_threshold['Time'] < gap_times_min.iloc[3]) & (vout_within_min_threshold['Time'] > gap_times_min.iloc[2])]
print("Selected min data:", selected_min_data)
min_avg = selected_min_data['vout'].mean()
print("Min average:", min_avg)
selected_max_data = vout_within_max_threshold[(vout_within_max_threshold['Time'] < gap_times_max.iloc[3]) & (vout_within_max_threshold['Time'] > gap_times_max.iloc[2])]
print("Selected max data:", selected_max_data)
max_avg = selected_max_data['vout'].mean()
print("Max average:", max_avg)
total_avg = (min_avg + max_avg) / 2
print("Total average:", total_avg)
# Plot the rest with different color
other_indices = df.index.difference(vout_within_min_threshold.index.union(vout_within_max_threshold.index))
print("Other indices:", df.loc[other_indices])
other_indices_data = df.loc[other_indices]
print("Other indices data:", other_indices_data['Time'])
# print th other indices time is between the second min gap time and the second max gap time
selected_points = other_indices_data[(other_indices_data['Time'] > min_second_gap_time) & (other_indices_data['Time'] < max_second_gap_time)]
if selected_points.empty:
    selected_points = other_indices_data[(other_indices_data['Time'] < min_second_gap_time) & (other_indices_data['Time'] > max_second_gap_time)]
print("Selected points:", selected_points)
# fit a line to the vout values of the selected points and save parameters for further use
# y = mx + c
# m = (nΣxy - ΣxΣy) / (nΣx^2 - (Σx)^2)
# c = (Σy - mΣx) / n
n = len(selected_points)
x = selected_points['Time']
y = selected_points['vout']
m = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (n * np.sum(x ** 2) - (np.sum(x)) ** 2)
c = (np.sum(y) - m * np.sum(x)) / n
# find the time value at the total_avg time
total_avg_time = (total_avg - c) / m
print("Total average time:", total_avg_time)
plt.scatter(df.loc[other_indices, 'Time'], df.loc[other_indices, 'vout'], color='blue', label='Other', marker='o')

plt.xlabel('Time')
plt.ylabel('vout')
plt.title('vout vs Time')
plt.grid(True)
plt.legend()
plt.show()
