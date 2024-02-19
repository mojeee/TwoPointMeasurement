import streamlit as st
import zipfile
import os
from io import BytesIO

def main():
    st.title("Zip File Upload and Extraction")

    # File Upload
    uploaded_file = st.file_uploader("Choose a zip file", type="zip")

    if uploaded_file is not None:
        # Display the uploaded file details
        st.subheader("Uploaded File Details:")
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)

        # Unzip the file
        with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
            # Choose a folder to extract the contents (you can modify this path as needed)
            extract_folder = "extracted_files"
            os.makedirs(extract_folder, exist_ok=True)
            zip_ref.extractall(extract_folder)

        st.success("File extraction complete!")

        # Display the list of files in the extracted folder
        st.subheader("List of Files in Extracted Folder:")
        for root, dirs, files in os.walk(extract_folder):
            for file in files:
                st.write(os.path.join(root, file))

        # Display the folder path
        st.subheader("Folder Path:")
        st.write(os.path.abspath(extract_folder))

# Run the app
if __name__ == "__main__":
    main()
