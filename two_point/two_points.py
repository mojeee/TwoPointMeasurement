import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os
import random


def get_random_color():
    # Generate a random color in the format "#RRGGBB"
    return "#{:02x}{:02x}{:02x}".format(
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    )


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

    def prep_plot(self, seprate_plot):
        self.seperate_plot = seprate_plot
        target_ending = "2-Point.txt"
        matching_files = [
            file for file in self.file_names if file.endswith(target_ending)
        ]
        if matching_files:
            print(f"Files ending with '{target_ending}' exist in the folder:")
            for file in matching_files:
                print(file)
                name = file[:-4]
                print(name)
                data = self.extract_data(file_name=file)
                self.plot_all(data=data, name=name)
        else:
            print(f"No files ending with '{target_ending}' found in the folder.")
        plt.show()

    def extract_data(self, file_name):
        with open(self.folder_path + file_name, "r") as file:
            lines = file.readlines()

        data = pd.DataFrame(
            [line.split() for line in lines[11:]],
            columns=["VD", "ID", "IG", "VG", "VS", "IS"],
        )

        data = data.apply(pd.to_numeric, errors="coerce")

        return data

    def plot_all(self, data, name, log_plot: bool = False, save_fig: bool = False):
        if self.seperate_plot:
            plt.figure()

        plt.plot(
            data["VD"],
            data["ID"],
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
        if save_fig and self.seperate_plot:
            pass


new = TwoPoints(
    folder_path="/Users/amini_m/Desktop/repo/twoPoint/data/112323_Ghazal_EGTs_Standard M7_2point/"
)
new.prep_plot(seprate_plot=True)
