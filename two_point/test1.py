import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

folder_path = "C:/Users/ghaza/OneDrive/Desktop/thesis/20230629_Ghazal_100_EGTs_M7_W_200_L20/"
file_names = [
    f
    for f in os.listdir(folder_path)
    if os.path.isfile(os.path.join(folder_path, f))
]

target_file_name = []
all_data = {}
for name in file_names:
    print(f"Processing file: {name}")
    
    if name.endswith("IV.txt"):
        with open(os.path.join(folder_path, name), "r") as file:
            lines = file.readlines()
        target_file_name.append(name)
        data = pd.DataFrame(
            [line.split() for line in lines[8:]],
            columns=["VD", "ID", "IG", "VG", "VS", "IS"],
        )
        
        data = data.apply(pd.to_numeric, errors="coerce")
        data['ID'] = data['ID']
        all_data[name] = data

target_file_name = st.multiselect("Select files", target_file_name)  
st.write("You selected", data[target_file_name])