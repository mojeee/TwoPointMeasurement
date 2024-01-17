import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

folder_path = "C:/Users/ghaza/OneDrive/Desktop/thesis/20230629_Ghazal_100_EGTs_M7_W_200_L20/"
file_names = [
    f
    for f in os.listdir(folder_path)
    if os.path.isfile(os.path.join(folder_path, f))
]


all_min_ids = []

for name in file_names:
    if name.endswith("IV.txt"):
        with open(os.path.join(folder_path, name), "r") as file:
            lines = file.readlines()

        data = pd.DataFrame(
            [line.split() for line in lines[8:]],
            columns=["VD", "ID", "IG", "VG", "VS", "IS"],
        )
        data = data.apply(pd.to_numeric, errors="coerce")
        data['ID'] = data['ID'].abs()

        all_min_ids.append(data['ID'].min())


#print min of all min ids
print(min(all_min_ids))
#print file name with min of all min
print(file_names[all_min_ids.index(min(all_min_ids))])
#plot iv vs id of all files
