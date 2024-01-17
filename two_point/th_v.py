import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import FuncFormatter
import os
import random
import math
import streamlit as st

def get_random_color():
    # Generate a random color in the format "#RRGGBB"
    return "#{:02x}{:02x}{:02x}".format(
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    )

class FindVth:
    def __init__(self, folder_path):
        st.title("Find Threshold Voltage")
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
    ):
        self.seperate_plot = seprate_plot
        target_ending = "trans.txt"
        matching_files = [
            file for file in self.file_names if file.endswith(target_ending)
        ]
        all_data = []
        thershold_voltage = []
        if matching_files:
            print(f"Files ending with '{target_ending}' exist in the folder:")
            for file in matching_files:
                if file in exception_files:
                    continue
                print(file)
                name = file[:-4]
                print(name)
                data = self._extract_data(file_name=file)
                
                thershold_voltage.append(self._find_v_thershold(data=data))
        else:
            print(f"No files ending with '{target_ending}' found in the folder.")

        # Calculate mean and variance
            #shift mean to 0.1 to avoid negative values
        thershold_voltage = np.array(thershold_voltage) + 0.015
        mean_vth = np.mean(thershold_voltage)
        var_vth = np.var(thershold_voltage)

        # Plot histogram of threshold voltage
        fig, ax = plt.subplots(figsize=(10, 6))  # Adjust figure size as needed
        ax.hist(thershold_voltage, bins=20, color='#86bf91', edgecolor='black', linewidth=1.2)
        ax.set_title('Distribution of Threshold Voltage', fontsize=16)
        ax.set_xlabel('Threshold Voltage (V)', fontsize=14)
        ax.set_ylabel('Frequency', fontsize=14)
        ax.axvline(mean_vth, color='r', linestyle='dashed', linewidth=2, label=f'Mean = {mean_vth:.2f}')
        ax.legend()

        # Add information about mean and variance
        st.text(f"Mean Threshold Voltage: {mean_vth:.2f}")
        st.text(f"Variance of Threshold Voltage: {var_vth:.2f}")

        # Annotate mean and variance on the plot with a soft box
        annotation_box_mean = dict(boxstyle="round,pad=0.3", edgecolor='none', facecolor='#87CEEB', alpha=0.7)
        annotation_box_var = dict(boxstyle="round,pad=0.3", edgecolor='none', facecolor='#87CEEB', alpha=0.7)

        ax.annotate(f'Mean = {mean_vth:.2f}', xy=(mean_vth, 0), xytext=(mean_vth, ax.get_ylim()[1]*0.9),
                    arrowprops=dict(facecolor='black', arrowstyle='wedge,tail_width=0.7', alpha=0.5),
                    fontsize=12, color='black', ha='center', bbox=annotation_box_mean)
        ax.annotate(f'Variance = {var_vth:.2f}', xy=(mean_vth, 0), xytext=(mean_vth, ax.get_ylim()[1]*0.85),
                    arrowprops=dict(facecolor='black', arrowstyle='wedge,tail_width=0.7', alpha=0.5),
                    fontsize=12, color='black', ha='center', bbox=annotation_box_var)

        # Display the plot in Streamlit
        ax.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig)
        plt.savefig('thershold_histogram.png', dpi=300, bbox_inches='tight')

            # Add a button to download the plot as a PNG file
        with open("thershold_histogram.png", "rb") as file:
            btn = st.download_button(
                        label="Download image",
                        data=file,
                            file_name="thershold_histogram.png",
                            mime="image/png"
                        )

    def _extract_data(self, file_name):
        with open(os.path.join(self.folder_path, file_name), "r") as file:
            lines = file.readlines()

        data = pd.DataFrame(
            [line.split() for line in lines[8:]],
            columns=["VG", "ID", "IG", "VD", "VS", "IS"],
        )

        data = data.apply(pd.to_numeric, errors="coerce")

        return data

    def _find_v_thershold(self, data):
        data['sqrt_ID'] = np.sqrt(np.abs(data['ID']))
        data = data[data['VD'] == data['VD'].max()]
        slope = data['sqrt_ID'].diff() / data['VG'].diff()
        # remove inf slope values from data
        slope = slope.replace([np.inf, -np.inf], 0)
        max_slope = np.max(slope)
        max_slope_index = np.argmax(slope)
        data_max_slope = data.iloc[max_slope_index]
        vg = data_max_slope['VG']   
        sqrt_id = data_max_slope['sqrt_ID']
        v_th = vg - sqrt_id / max_slope 

        return v_th
