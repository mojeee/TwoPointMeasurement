import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from two_point.logicgate import LogicGates
from two_point.inverterpulldown import InverterDataProcessor
from two_point.inverter_main import Inverter
from two_point.th_v import FindVth
import zipfile
import os
import shutil

def unzip_and_display_files(uploaded_file):
    # Unzip the file
    with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
        # Choose a folder to extract the contents (you can modify this path as needed)
        extract_folder = "extracted_files/"
        os.makedirs(extract_folder, exist_ok=True)
        zip_ref.extractall(extract_folder)

    st.success("File extraction complete!")
    
    zip_file_folder_path = os.path.abspath(extract_folder).replace("\\", "/") + "/" + uploaded_file.name[:-4] + "/"
    return zip_file_folder_path

def delete_temporary_files(folder_path):
    # Delete the temporary folder and its contents
    shutil.rmtree(folder_path)

def main():
    st.title("KIT INT Application")

    report_type = st.sidebar.selectbox("Select a Report Type", ("Invertergain","Logic Gates", "Thershhold Voltage", "Inverter Pull Up an Down","Ioffmean","Ioff"))

    if report_type == "Invertergain":
        uploaded_file = st.file_uploader("Upload a zip file", type="zip")

        if uploaded_file is not None:
            st.subheader("Uploaded File Details:")
            file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
            #st.write(file_details)

            # Call the function to unzip and display files
            zip_file_folder_path = unzip_and_display_files(uploaded_file)
            st.write(zip_file_folder_path)
            summary_plot = st.sidebar.checkbox('Summary Plot')
            seperate_plot = st.sidebar.checkbox('Seperate Plot')
            gain_plot = st.sidebar.checkbox('Gain Plot')
            inverterplot = Inverter(
            folder_path=zip_file_folder_path
            )
            inverterplot.prep_plot(
                summary_plot=summary_plot,
                seprate_plot=seperate_plot,
                gain_plot=gain_plot,
                exception_files=[]
            )


    if report_type == "Logic Gates":
        logicg = LogicGates()
        logicg.plot_logic_gate()

    elif report_type == "Thershhold Voltage":

         # File Upload for zip files
        uploaded_file = st.file_uploader("Upload a zip file", type="zip")

        if uploaded_file is not None:
            st.subheader("Uploaded File Details:")
            file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
            #st.write(file_details)

            # Call the function to unzip and display files
            zip_file_folder_path = unzip_and_display_files(uploaded_file)
            st.write(zip_file_folder_path)
       
            inverterplot = FindVth(
                folder_path=zip_file_folder_path
            )
            inverterplot.prep_plot(
                exception_files=[]
            )

            # Delete temporary files after use
            delete_temporary_files(zip_file_folder_path)

    elif report_type == "Inverter Pull Up an Down":
        uploaded_file = st.file_uploader("Upload a zip file", type="zip")

        if uploaded_file is not None:
            st.subheader("Uploaded File Details:")
            file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
            #st.write(file_details)

            # Call the function to unzip and display files
            zip_file_folder_path = unzip_and_display_files(uploaded_file)
            st.write(zip_file_folder_path)
            inverter_processor = InverterDataProcessor(zip_file_folder_path)
            inverter_processor.process_files()
            mean_min_Vout , mean_max_Vout = inverter_processor.calculate_mean_min_Vout()
            st.write(f"Mean of minimum Vout: {mean_min_Vout}")
            st.write(f"Mean of maximum Vout: {mean_max_Vout}")

    elif report_type == "Ioffmean":
        pass

    elif report_type == "Ioff":
        pass

# Run the app
if __name__ == "__main__":
    main()
