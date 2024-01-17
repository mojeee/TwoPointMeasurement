import os
import pandas as pd
import matplotlib.pyplot as plt


folder_path = "C:/Users/ghaza/OneDrive/Desktop/profil/ZNO"

# List all files in the folder
files = os.listdir(folder_path)

# Filter only CSV files
csv_files = [file for file in files if file.endswith(".csv")]

# Check if there are any CSV files
if csv_files:
    # Read the first CSV file
    first_csv_file_path = os.path.join(folder_path, csv_files[0])

    # Create a dictionary to store variable and value pairs
    data_dict = {}
    um = []
    area = []
    with open(first_csv_file_path, 'r') as file:
        # Read and store the first 35 rows in the dictionary
        row_counter = 1
        for row in file:
            line = row.strip().split(',')
            
            if row_counter <= 35:
                variable, value = line[0], line[1]
                data_dict[variable] = value
            elif row_counter >36:
                #print(row, end='')
                try:
                    um.append(line[0])
                    area.append(line[1])
                except:
                    pass
            row_counter+=1

# Print the DataFrame
df = pd.DataFrame(list(zip(um, area)), columns=['Area', 'Um'])

print(df.shape)

plt.plot(df.Um,df.Area)
plt.show()
# Print the dictionary
#print(data_dict)











'''from two_point.two_points_copy import DiodeMeas

twopoint = DiodeMeas(
    folder_path="C:/Users/ghaza/OneDrive/Desktop/repo/TwoPointMeasurement/data/20231114/"
)
twopoint.read_excel_file()'''
