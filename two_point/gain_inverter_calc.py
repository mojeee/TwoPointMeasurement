import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

folder_path = "C:/Users/Hiva/Desktop/Virevo-project/TwoPointMeasurement/data/nor"
file_names = [
    f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))
]
print(file_names)

for file in file_names:
    path = os.path.join(folder_path, file)
    df = pd.read_csv(path, sep="\t", decimal=",", thousands=None, engine="python")

    df = df.applymap(
        lambda x: x.replace(",", ".").replace("E", "e") if isinstance(x, str) else x
    )
    df = df.apply(pd.to_numeric, errors="coerce")
    if len(df.columns) == 4:
        df.columns = ["Time", "Vin", "Vin2", "Vout"]
    elif len(df.columns) == 2:
        df.columns = ["Vin", "Vout"]
       
    #print(df.head())
    #df = df[(df["Time"] > 1.5)&(df["Time"] < 2.3)]
    df["Vout/Vin"] = np.gradient(df["Vout"], df["Vin"])
    print(df['Vout/Vin'])
    # scatter plot vout/vin vs vin
    plt.plot(df["Vin"], df["Vout/Vin"])
    plt.xlabel("Vin")
    plt.ylabel("Vout/Vin")
    plt.title("Vout/Vin vs Vin")
    plt.show()

    
    
