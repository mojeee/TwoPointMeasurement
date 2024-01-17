# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 15:10:35 2023

@author: ep4099

"""


 #-*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#%%
##if encounter"AttributeError: module 'win32com.gen_py.00020813-0000-0000-C000-000000000046x0x1x9' has no attribute 'MinorVersion'"
##uncomment following codes and run it, to delete the "gen_py" and restart spyder
##After restart spyder remenber to comment following codes
# import win32com
# import shutil
# shutil.rmtree(r'C:\Users\ep4099\AppData\Local\Temp\gen_py')
#%%
#precondition
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import os.path
import win32com.client as win32 ## when error occurs, find gen_py with "print(win32com.__gen_path__)" and delete it
from openpyxl import load_workbook
import shutil
import pandas as pd
#%%
##tpye the root dir
rootdir = os.path.dirname(__file__) #path of the directory under processed
#%%
# save file as .xlsx
#build filedirlist
excel_op = win32.gencache.EnsureDispatch('Excel.Application')#open Excel
for root, dirs, files in os.walk(rootdir, topdown=True):
    for name in files:
       if name.endswith("xls"):
            exceldir = os.path.join(root, name)
            wb = excel_op.Workbooks.Open(exceldir)#open excel_file
            wb.Application.DisplayAlerts = False #turn off the inquiry dialog
            wb.Worksheets('Calc').Delete()#delete sheets
            wb.Worksheets('Settings').Delete()#delete sheets
            wb.Application.DisplayAlerts = True# turn on the inquiry dialog
            wb.SaveAs(exceldir.replace('xls', 'xlsx'),FileFormat=51)#file resave as xlsx
          #xlsx:FileFormat=51
#         #xls:FileFormat=56
            wb.Close()# close workbook
            os.remove(exceldir)#delete the .xlsx file
       else:
         continue
'''
#%%
##plot Initial sweep curves
for root, dirs, files in os.walk(rootdir, topdown=True):
    for name in dirs:
        device_dir = os.path.join(root, name)##build path of "device" directory
        files = os.listdir(device_dir)
        for file in files:
            if file.endswith("xlsx") and "Initial sweep_forward" in file:
                ws_file_dir = os.path.join(root, name, file)
                var = pd.read_excel(ws_file_dir)
                x = list(var["AV"])
                y = list(var["AI"])
                plt.figure()
                plt.plot(x,y)
                plt.xlabel('Voltage/V',fontsize=10)
                plt.ylabel('Current/A',fontsize=10)
                plt.xticks(fontsize=10)
                plt.yticks(fontsize=10)
                plt.title(name+"/Initial sweeping")
                plt.show()


        else:
            continue
#%%
##plot Initial sweep curves (plot linear + logy)
for root, dirs, files in os.walk(rootdir, topdown=True):
    for name in dirs:
        device_dir = os.path.join(root, name)##build path of "device" directory
        files = os.listdir(device_dir)
        for file in files:
            if file.endswith("xlsx") and "Initial sweep_forward" in file:
                ws_file_dir = os.path.join(root, name, file)
                var = pd.read_excel(ws_file_dir)
                x = list(var["AV"])
                y = list(var["AI"])
                y_abs = list (map(abs, y))
                fig, ax1 = plt.subplots()
                ax1.set_xlabel('Voltage/V', fontsize=10)
                ax1.set_ylabel('Current/A', fontsize=10, color='red')
                ax1.plot(x, y, color='red')
                ax1.tick_params(axis='y', labelcolor='red')

                ax2 = ax1.twinx()
                ax2.set_ylabel('Current/A', fontsize=10, color='blue')
                ax2.plot(x, y_abs, color='blue')
                ax2.tick_params(axis='y', labelcolor='blue')
                ax2.set_yscale('log')

                plt.title(name+"/Initial sweeping")
                # plt.yscale('log')
                plt.show()


        else:
            continue
'''