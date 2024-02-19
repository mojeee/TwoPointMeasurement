import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

folder_path = "C:/Users/ghaza/OneDrive/Desktop/thesis/passgate/XOR/"
file_names = [
    f
    for f in os.listdir(folder_path)
    if os.path.isfile(os.path.join(folder_path, f))
]

all_max_Vout = []

for name in file_names:
    if name.endswith("transient_1,0V.dat"):
        with open(os.path.join(folder_path, name), "r") as file:
            lines = file.readlines()

        data = pd.DataFrame(
            [line.split() for line in lines[2:]],
            columns=["time [s]","Vin1 [V]","Vin2 [V]","Vout [V]"],
        )
        
        data = data.replace({',': '.'}, regex=True)

        print(data)
        data = data.apply(pd.to_numeric, errors="coerce")
        #print(data)
        all_max_Vout.append(data['Vout [V]'].max())
    
print(np.mean(all_max_Vout))
