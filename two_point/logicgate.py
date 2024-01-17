import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64


class LogicGates:
    def __init__(self) -> None:
        st.title("Logic Gates")
        self.df = None
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            # read text file line by line and store it into a dataframe
            df = pd.read_csv(uploaded_file, sep='\t', decimal=',', thousands=None, engine='python')

            # Replace commas with dots and update scientific notation
            df = df.applymap(lambda x: x.replace(',', '.').replace('E', 'e') if isinstance(x, str) else x)
            df = df.apply(pd.to_numeric, errors='coerce')
        
            df.columns = ['Time', 'Vin1', 'Vin2', 'Vout']
            self.df = df
    def plot_logic_gate(self,):
        # plot all columns vs time in a plot (3,1)
        if self.df is None:
            st.write("Please upload a file")
        else:
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))  # Adjust figure size as needed
            # add plot title
            title = st.text_input('Plot Title', 'Logic Gates')
            #fig.suptitle(title, fontsize=12)
            # fit a line to min of plots
            ax1.plot(self.df['Time'], self.df['Vin1'], color='blue', label='Vin1')
            ax1.axhline(y=0, color='black', linestyle='--', linewidth=1)
            ax1.axhline(y=1, color='black', linestyle='--', linewidth=1)
            ax1.set_ylabel('Vin1 (V)')
            #add title to plot
            ax1.set_title(title, fontsize=16)
            # turn off x-axis ticks
            ax2.plot(self.df['Time'], self.df['Vin2'], color='green', label='Vin2')
            ax2.axhline(y=0, color='black', linestyle='--', linewidth=1)
            ax2.axhline(y=1, color='black', linestyle='--', linewidth=1)
            ax2.set_ylabel('Vin2 (V)')
            # turn off x-axis ticks
            ax3.plot(self.df['Time'], self.df['Vout'], color='red', label='Vout')
            ax3.axhline(y=0, color='black', linestyle='--', linewidth=1)
            ax3.axhline(y=1, color='black', linestyle='--', linewidth=1)
            ax3.set_ylabel('Vout (V)')
            ax3.set_xlabel('Time (S)')

            ax1.grid(True, linestyle='--', alpha=0.6)
            ax2.grid(True, linestyle='--', alpha=0.6)
            ax3.grid(True, linestyle='--', alpha=0.6)

            # Display the plot
            st.pyplot(fig)
            # save plot as png file
            plt.savefig('logicgate.png', dpi=300, bbox_inches='tight')

            # Add a button to download the plot as a PNG file
            with open("logicgate.png", "rb") as file:
                btn = st.download_button(
                        label="Download image",
                        data=file,
                            file_name="logicgate.png",
                            mime="image/png"
                        )
