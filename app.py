import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from two_point.logicgate import LogicGates
from two_point.th_v import FindVth

report_type = st.sidebar.selectbox("Select a Report Type", ("Logic Gates", "Thershhold Voltage", "Inverter Pull Down","Inverter Pull Up","Ioffmean","Ioff"))
if report_type == "Logic Gates":
    logicg = LogicGates()
    logicg.plot_logic_gate()
elif report_type == "Thershhold Voltage":

    agree = st.sidebar.checkbox('Set a New Folder Path')

    if agree:
        new_folder_path = st.sidebar.text_input('New Folder Path', 'Paste the new folder path here')
        inverterplot = FindVth(
            folder_path= new_folder_path
        )
        inverterplot.prep_plot(
            seprate_plot=True,
            exception_files=[]
        )

    else:
        inverterplot = FindVth(
            folder_path="C:/Users/ghaza/OneDrive/Desktop/thesis/20230629_Ghazal_100_EGTs_M7_W_200_L20/"
        )
        inverterplot.prep_plot(
            seprate_plot=True,
            exception_files=[]
        )