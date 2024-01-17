from Inverter import Inverter
import matplotlib.pyplot as plt

inverterplot = Inverter(
    folder_path="C:/Users/ghaza/OneDrive/Desktop/thesis/invertergain/"
)
inverterplot.prep_plot(
    #summary_plot=True,
    seprate_plot=True,
    gain_plot=True,
    exception_files=[]
)
