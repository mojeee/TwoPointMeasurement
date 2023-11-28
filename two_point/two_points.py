import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os
import random

def plot_all(file, name, folder, log_plot: bool = False):
    with open(folder + file, "r") as file:
        lines = file.readlines()

    # Create DataFrames
    header_part1 = lines[8].split()[:4]
    data_part = pd.DataFrame([line.split()[:4] for line in lines[:9]], columns=header_part1)
    data_part1 = pd.DataFrame({
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
    })
    data_part2 = pd.DataFrame(
        [line.split() for line in lines[11:]],
        columns=["VD", "ID", "IG", "VG", "VS", "IS"],
    )

    # Plot IV vs ID with random color
    data_part2 = data_part2.apply(pd.to_numeric, errors="coerce")
    plt.plot(
        data_part2["VD"],
        data_part2["ID"],
        label="ID vs VD",
        marker="s",
        linestyle="-",
        color=get_random_color(),
    )

    if log_plot:
        plt.yscale("log")

    plt.xlabel("VD (V)")
    plt.ylabel("ID (A)")
    plt.title("VD vs ID Plot")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()

def get_random_color():
    # Generate a random color in the format "#RRGGBB"
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class TwoPoints:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        try:
            # Get all file names in the folder
            self.file_names = [
                f
                for f in os.listdir(self.folder_path)
                if os.path.isfile(os.path.join(self.folder_path, f))
            ]
            print(self.file_names)
        except Exception as e:
            print(f"An error occurred: {e}")


new = TwoPoints(
    folder_path="/Users/amini_m/Desktop/repo/twoPoint/data/112323_Ghazal_EGTs_Standard M7_2point/"
)
target_ending = "2-Point.txt"

matching_files = [file for file in new.file_names if file.endswith(target_ending)]
folder_path = (
    "/Users/amini_m/Desktop/repo/twoPoint/data/112323_Ghazal_EGTs_Standard M7_2point/"
)
# Print messages based on the results
if matching_files:
    print(f"Files ending with '{target_ending}' exist in the folder:")
    for file in matching_files:
        print(file)
        name = file[:-4]
        print(name)
        plot_all(file=file, name=name, folder=folder_path)
else:
    print(f"No files ending with '{target_ending}' found in the folder.")

# Open the file in read mode
"""file_path = (
    "data/M10H2_2-Point.txt"  # Replace 'your_file.txt' with the actual file path
)"""


plt.show()
