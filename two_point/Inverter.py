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


class Inverter:
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
        gain_plot : bool = False,
    ):
        self.seperate_plot = seprate_plot
        self.gain_plot = gain_plot
        target_ending = "Inverter.txt"
        matching_files = [
            file for file in self.file_names if file.endswith(target_ending)
        ]
        all_data = []
        max_abs_values = []
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
                if not gain_plot:
                    all_data.append(data["Vout"].values)
                else:
                    all_data.append(data["Vout/Vin"].values)
                
                max_abs_values.append(np.max(np.abs(data["Vout/Vin"])))
            print("Mean of max absolute values: ", np.mean(max_abs_values))

        else:
            print(f"No files ending with '{target_ending}' found in the folder.")
        mean_data = np.mean(all_data, axis=0)
        std_data = np.std(all_data, axis=0)
        if summary_plot:
            self._plot_mean_std(data=data, mean_data=mean_data, std_data=std_data)
       
        if not seprate_plot:
            if self.gain_plot:
                plt.savefig(os.path.join(self.folder_path, "all_plots"+ "_gain" + ".png"))
            else:
                plt.savefig(os.path.join(self.folder_path, "all_plots" + ".png"))
        else:
            if self.gain_plot:
                plt.savefig(os.path.join(self.folder_path, "summary_plots"+ "_gain" + ".png"))
            else:
                plt.savefig(os.path.join(self.folder_path, "summary_plots" + ".png"))

        plt.show()

    def _extract_data(self, file_name):
        with open(self.folder_path + file_name, "r") as file:
            lines = file.readlines()

        data = pd.DataFrame(
            [line.split() for line in lines[8:]],
            columns=["Vin", "Vout"],
        )
        data = data.apply(pd.to_numeric, errors="coerce")
        #data["Vout/Vin"] = data['Vout'].diff() / data['Vin'].diff()
        data["Vout/Vin"] =  np.gradient(data['Vout'],data['Vin'])
    

        return data

    def _plot_all(self, data, name, save_fig: bool = False):
        if self.seperate_plot:
            plt.figure()
        
        if self.gain_plot:
            plt.plot(
                data["Vin"],
                data["Vout/Vin"],
                label="Vout/Vin vs Vin",
                marker="s",
                linestyle="-",
                color=get_random_color(),
            )
            plt.xlabel("Vin (V)")
            plt.ylabel("Vout/Vin (V)")
            plt.title("Vout/Vin vs Vin Plot")
        else: 
            plt.plot(
                data["Vin"],
                data["Vout"],
                label="Vout vs Vin",
                marker="s",
                linestyle="-",
                color=get_random_color(),
            )
            plt.xlabel("Vin (V)")
            plt.ylabel("Vout (V)")
            plt.title("Vout vs Vin Plot")

        
        #plt.yscale("log")

        
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.tight_layout()
        if self.seperate_plot:
            if self.gain_plot:
                plt.savefig(os.path.join(self.folder_path, name +"_gain" + ".png"))
            else:
                plt.savefig(os.path.join(self.folder_path, name + ".png"))

    def _plot_mean_std(self, data, mean_data, std_data, log_plot: bool = False):
        plt.figure()
        plt.plot(data["Vin"], mean_data, label="Mean gain", color="b", linestyle="-")

        if log_plot:
            plt.yscale("log")

        plt.fill_between(
            data["Vin"],
            mean_data - std_data,
            mean_data + std_data,
            alpha=0.3,
            color="b",
            label="Std Dev",
        )

        plt.xlabel("Vin (V)")
        if self.gain_plot:
            plt.ylabel("Vout/Vin (V)")
            plt.title("Mean Vout/Vin with Std Dev Plot")
        else:
            plt.ylabel("Vout (V)")
            plt.title("Mean Vout with Std Dev Plot")

        plt.grid(True, linestyle="--", alpha=0.7)
        plt.legend()
        plt.tight_layout()
        





