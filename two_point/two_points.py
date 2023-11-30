import pandas as pd
import numpy as np
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

    def prep_plot(
        self,
        exception_files,
        seprate_plot: bool = False,
        summary_plot: bool = False,
        save_plot: bool = False,
    ):
        self.seperate_plot = seprate_plot
        target_ending = "2-Point.txt"
        matching_files = [
            file for file in self.file_names if file.endswith(target_ending)
        ]
        all_data = []
        if matching_files:
            print(f"Files ending with '{target_ending}' exist in the folder:")
            for file in matching_files:
                if file in exception_files:
                    continue
                print(file)
                name = file[:-4]
                print(name)
                data = self._extract_data(file_name=file)
                if not summary_plot:
                    self._plot_all(data=data, name=name)
                all_data.append(data["ID"].values)
        else:
            print(f"No files ending with '{target_ending}' found in the folder.")
        mean_data = np.mean(all_data, axis=0)
        std_data = np.std(all_data, axis=0)
        if summary_plot:
            self._plot_mean_std(data=data, mean_data=mean_data, std_data=std_data)
        if save_plot:
            if not seprate_plot:
                plt.savefig(os.path.join(self.folder_path, "all_plots" + ".png"))
            else:
                plt.savefig(os.path.join(self.folder_path, "summary_plots" + ".png"))

        plt.show()

    def _extract_data(self, file_name):
        with open(self.folder_path + file_name, "r") as file:
            lines = file.readlines()

        data = pd.DataFrame(
            [line.split() for line in lines[11:]],
            columns=["VD", "ID", "IG", "VG", "VS", "IS"],
        )

        data = data.apply(pd.to_numeric, errors="coerce")

        return data

    def _plot_all(self, data, name, save_fig: bool = False):
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

        
        #plt.yscale("log")

        plt.xlabel("VD (V)")
        plt.ylabel("ID (A)")
        plt.title("VD vs ID Plot")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.tight_layout()
        if save_fig and self.seperate_plot:
            plt.savefig(os.path.join(self.folder_path, name + ".png"))

    def _plot_mean_std(self, data, mean_data, std_data, log_plot: bool = False):
        plt.figure()
        plt.plot(data["VD"], mean_data, label="Mean ID", color="b", linestyle="-")

        if log_plot:
            plt.yscale("log")

        plt.fill_between(
            data["VD"],
            mean_data - std_data,
            mean_data + std_data,
            alpha=0.3,
            color="b",
            label="Std Dev",
        )

        plt.xlabel("VD (V)")
        plt.ylabel("ID (A)")
        plt.title("Mean ID with Std Dev Plot")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.legend()
        plt.tight_layout()
