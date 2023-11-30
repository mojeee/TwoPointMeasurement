import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.animation import FuncAnimation
import os
import random


def get_random_color():
    # Generate a random color in the format "#RRGGBB"
    return "#{:02x}{:02x}{:02x}".format(
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    )


import os

class DiodeMeas:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        all_excel_files = {}
        self.all_excel_file_path =[]
        

        try:
            # Get all folder names in the main folder
            self.folder_names = [
                d
                for d in os.listdir(self.folder_path)
                if os.path.isdir(os.path.join(self.folder_path, d))
            ]

            # Iterate through each folder and get file names
            for folder_name in self.folder_names:
                folder_path = os.path.join(self.folder_path, folder_name)
                file_names = [
                    f
                    for f in os.listdir(folder_path)
                    if os.path.isfile(os.path.join(folder_path, f))
                ]
                all_excel_files[folder_name]= file_names

            for folder in all_excel_files.keys():
                all_file = all_excel_files[folder]
                target_ending = ".xlsx"
                matching_files = [file for file in all_file if file.endswith(target_ending)]
                matching_fil = [file for file in matching_files if file[8:13] == 'sweep']
                #print(folder +'/' +matching_fil[0])
                self.all_excel_file_path.append(folder +'/' +matching_fil[0])
            
            print(self.all_excel_file_path)
            '''target_ending = ".xlsx"
            matching_files = [file for file in all_excel_files if file.endswith(target_ending)]
            matching_fil = [file for file in matching_files if file[8:13] == 'sweep']
            print(matching_fil)
            self.all_file_names = matching_fil'''

        except Exception as e:
            print(f"An error occurred: {e}")

    def read_excel_file(self):
    
        for excel_file in self.all_excel_file_path:
            data = pd.read_excel(os.path.join(self.folder_path, excel_file))
            # Print or manipulate the DataFrame as needed
            #print(data["AV"])
            plt.plot(data["AV"],abs(data["AI"]),label="AI vs AV",linestyle="-",color=get_random_color())
            plt.yscale("log")

        plt.xlabel("AV (V)")
        plt.ylabel("AI (A)")
        plt.title("AI vs AV Plot")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(self.folder_path, 'all_fig' + ".png"))
        plt.show()

