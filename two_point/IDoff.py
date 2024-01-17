import os
import pandas as pd
import matplotlib.pyplot as plt

folder_path = "C:/Users/ghaza/OneDrive/Desktop/thesis/20230629_Ghazal_100_EGTs_M7_W_200_L20/"
file_names = [
    f
    for f in os.listdir(folder_path)
    if os.path.isfile(os.path.join(folder_path, f))
]

all_min_ids = []

for name in file_names:
    if name.endswith("IV.txt"):
        with open(os.path.join(folder_path, name), "r") as file:
            lines = file.readlines()

        data = pd.DataFrame(
            [line.split() for line in lines[8:]],
            columns=["VD", "ID", "IG", "VG", "VS", "IS"],
        )
        data = data.apply(pd.to_numeric, errors="coerce")
        data['ID'] = data['ID'].abs()

        all_min_ids.append(data['ID'].min())

# Create a histogram with customized settings
plt.hist(all_min_ids, bins=20, color='skyblue', edgecolor='black')

# Add labels and title
plt.xlabel(' $I_{Off}$ (A)')
plt.ylabel('Frequency')
plt.title('Distribution of $I_{Off}$')
plt.grid(True, linestyle='--', alpha=0.7)
# Add mean and variance information
mean_value = "{:e}".format(round(pd.Series(all_min_ids).mean(), 15))
variance_value = round(pd.Series(all_min_ids).var(), 20)
plt.text(0.60, 0.95, f'Mean: {mean_value}\nVariance: {variance_value}', transform=plt.gca().transAxes, fontsize=10,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Show the plot

# Save the plot to a file (adjust the filename and format as needed)
plt.savefig(os.path.join(folder_path, 'histogram_plot.png'))
plt.show()
