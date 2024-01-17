import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

class InverterDataProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.file_names = [
            f
            for f in os.listdir(self.folder_path)
            if os.path.isfile(os.path.join(self.folder_path, f))
        ]
        self.all_min_Vout = []
        self.all_max_Vout = []

    def process_files(self):
        for name in self.file_names:
            if name.endswith("Inverter.txt"):
                with open(os.path.join(self.folder_path, name), "r") as file:
                    lines = file.readlines()

                data = pd.DataFrame(
                    [line.split() for line in lines[8:]],
                    columns=["Vin", "Vout"],
                )
                data = data.apply(pd.to_numeric, errors="coerce")

                self.all_min_Vout.append(data['Vout'].min())
                self.all_max_Vout.append(data['Vout'].max())

    def calculate_mean_min_Vout(self):
        return np.mean(self.all_min_Vout), np.mean(self.all_max_Vout)

