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
vin1_min = df['vin1'].min()
vin1_max = df['vin1'].max()

# Define smaller thresholds
threshold_min = 0.15 * (vin1_max - vin1_min)
threshold_max = 0.15 * (vin1_max - vin1_min)

# Filter data within a threshold around min and max values
vin1_within_min_threshold = df[(df['vin1'] >= vin1_min) & (df['vin1'] <= vin1_min + threshold_min)]
vin1_within_max_threshold = df[(df['vin1'] >= vin1_max - threshold_max) & (df['vin1'] <= vin1_max)]
print("Data within Min Threshold:")
print (vin1_within_min_threshold)

# Plot vin1 against time
plt.figure(figsize=(10, 6))

# Plot raw data line
plt.plot(df['Time'], df['vin1'], color='gray', label='Raw Data')

# Mark individual points for different segments based on thresholding
plt.scatter(vin1_within_min_threshold['Time'], vin1_within_min_threshold['vin1'], color='red', label='Within Min Threshold', marker='o')
plt.scatter(vin1_within_max_threshold['Time'], vin1_within_max_threshold['vin1'], color='green', label='Within Max Threshold', marker='o')


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

gap_indices_min, gap_times_min = find_gap_indices(vin1_within_min_threshold)
gap_indices_max, gap_times_max = find_gap_indices(vin1_within_max_threshold)


print("Gap indices:", gap_indices_min)
print("Time values at the gaps:", gap_times_min)
print("Gap indices:", gap_indices_max)
print("Time values at the gaps:", gap_times_max)
min_second_gap_time = gap_times_min.iloc[1]
print("Second min gap time:", min_second_gap_time)
max_second_gap_time = gap_times_max.iloc[1]
print("Second max gap time:", max_second_gap_time)
selected_min_data = vin1_within_min_threshold[(vin1_within_min_threshold['Time'] < gap_times_min.iloc[2]) & (vin1_within_min_threshold['Time'] > gap_times_min.iloc[1])]
print("Selected min data:", selected_min_data)
min_avg = selected_min_data['vin1'].mean()
print("Min average:", min_avg)
selected_max_data = vin1_within_max_threshold[(vin1_within_max_threshold['Time'] < gap_times_max.iloc[2]) & (vin1_within_max_threshold['Time'] > gap_times_max.iloc[1])]
print("Selected max data:", selected_max_data)
max_avg = selected_max_data['vin1'].mean()
print("Max average:", max_avg)
total_avg = (min_avg + max_avg) / 2
print("Total average:", total_avg)
# Plot the rest with different color
other_indices = df.index.difference(vin1_within_min_threshold.index.union(vin1_within_max_threshold.index))
print("Other indices:", df.loc[other_indices])
other_indices_data = df.loc[other_indices]
print("Other indices data:", other_indices_data['Time'])
# print th other indices time is between the second min gap time and the second max gap time
selected_points = other_indices_data[(other_indices_data['Time'] > min_second_gap_time) & (other_indices_data['Time'] < max_second_gap_time)]
if selected_points.empty:
    selected_points = other_indices_data[(other_indices_data['Time'] < min_second_gap_time) & (other_indices_data['Time'] > max_second_gap_time)]
print("Selected points:", selected_points)
# fit a line to the vin1 values of the selected points and save parameters for further use
# y = mx + c
# m = (nΣxy - ΣxΣy) / (nΣx^2 - (Σx)^2)
# c = (Σy - mΣx) / n
n = len(selected_points)
x = selected_points['Time']
y = selected_points['vin1']
m = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (n * np.sum(x ** 2) - (np.sum(x)) ** 2)
c = (np.sum(y) - m * np.sum(x)) / n
# find the vin1 value at the total_avg time
# find the time value at the total_avg time
total_avg_time = (total_avg - c) / m
#print("Total average time:", total_avg_time)
if np.isnan(total_avg_time):
    total_avg_time = max([selected_min_data['Time'].min(), selected_max_data['Time'].min()])
    print("Total average time:", total_avg_time)



min_second_gap_time = gap_times_min.iloc[2]
print("Second min gap time:", min_second_gap_time)
max_second_gap_time = gap_times_max.iloc[2]
print("Second max gap time:", max_second_gap_time)
selected_min_data = vin1_within_min_threshold[(vin1_within_min_threshold['Time'] < gap_times_min.iloc[3]) & (vin1_within_min_threshold['Time'] > gap_times_min.iloc[2])]
print("Selected min data:", selected_min_data)
min_avg = selected_min_data['vin1'].mean()
print("Min average:", min_avg)
selected_max_data = vin1_within_max_threshold[(vin1_within_max_threshold['Time'] < gap_times_max.iloc[3]) & (vin1_within_max_threshold['Time'] > gap_times_max.iloc[2])]
print("Selected max data:", selected_max_data)
max_avg = selected_max_data['vin1'].mean()
print("Max average:", max_avg)
total_avg = (min_avg + max_avg) / 2
print("Total average:", total_avg)
# Plot the rest with different color
other_indices = df.index.difference(vin1_within_min_threshold.index.union(vin1_within_max_threshold.index))
print("Other indices:", df.loc[other_indices])
other_indices_data = df.loc[other_indices]
print("Other indices data:", other_indices_data['Time'])
# print th other indices time is between the second min gap time and the second max gap time
selected_points = other_indices_data[(other_indices_data['Time'] > min_second_gap_time) & (other_indices_data['Time'] < max_second_gap_time)]
if selected_points.empty:
    selected_points = other_indices_data[(other_indices_data['Time'] < min_second_gap_time) & (other_indices_data['Time'] > max_second_gap_time)]
print("Selected points:", selected_points)
# fit a line to the vin1 values of the selected points and save parameters for further use
# y = mx + c
# m = (nΣxy - ΣxΣy) / (nΣx^2 - (Σx)^2)
# c = (Σy - mΣx) / n
n = len(selected_points)
x = selected_points['Time']
y = selected_points['vin1']
m = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (n * np.sum(x ** 2) - (np.sum(x)) ** 2)
c = (np.sum(y) - m * np.sum(x)) / n
# find the vin1 value at the total_avg time
# find the time value at the total_avg time
total_avg_time = (total_avg - c) / m
#print("Total average time:", total_avg_time)
if np.isnan(total_avg_time):
    total_avg_time = max([selected_min_data['Time'].min(), selected_max_data['Time'].min()])
    print("Total average time:", total_avg_time)



plt.scatter(df.loc[other_indices, 'Time'], df.loc[other_indices, 'vin1'], color='blue', label='Other', marker='o')

plt.xlabel('Time')
plt.ylabel('vin1')
plt.title('vin1 vs Time')
plt.grid(True)
plt.legend()
plt.show()
