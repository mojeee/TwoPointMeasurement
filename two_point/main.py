import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Open the file in read mode
file_path = (
    "data/M10H2_2-Point.txt"  # Replace 'your_file.txt' with the actual file path
)
with open(file_path, "r") as file:
    lines = file.readlines()

# Create DataFrames
header_part1 = lines[8].split()[
    :4
]  # Extract the first four columns from the header line
data_part = pd.DataFrame([line.split()[:4] for line in lines[:9]], columns=header_part1)
data_part1 = pd.DataFrame(
    {
        "Setup Title": [data_part["IG"][0]],
        "Application": [data_part["ID"][1]],
        "Application Name": [data_part["VG"][1]],
        "Test Date": [data_part["IG"][2]],
        "Test Time": [data_part["IG"][3]],
        "Device ID": [data_part["IG"][4]],
        "Count": [data_part["ID"][5]],
        "Name": [data_part["VD"][7]],
        "Polarity": [data_part["ID"][7]],
        "Humidity": [data_part["IG"][7]],
        "W": [data_part["VG"][7]],
    }
)
data_part2 = pd.DataFrame(
    [line.split() for line in lines[11:]], columns=["VD", "ID", "IG", "VG", "VS", "IS"]
)

# Print the DataFrames
# print("Data Part 1:")
# print(data_part1)

# print("\nData Part 2:")
# print(data_part2)
# Plot IV vs ID
data_part2 = data_part2.apply(pd.to_numeric, errors='coerce')

plt.plot(
    data_part2["ID"],
    data_part2["VD"],
    label="VD vs ID",
    marker="o",
    linestyle="-",
    color="b",
)
plt.xlabel("ID")
plt.ylabel("VD")
plt.title("VD vs ID Plot")
plt.legend()
# Specify all "ID" values on the x-axis
plt.xticks(data_part2["ID"])

# Rotate x-axis ticks for better readability
plt.xticks(rotation=45, ha="right")

plt.grid(True, linestyle="--", alpha=0.7)
# Adjust layout for better spacing
plt.tight_layout()

plt.show()