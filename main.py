from two_point.two_points import TwoPoints

twopoint = TwoPoints(
    folder_path="C:/Users/ghaza/OneDrive/Desktop/MY THESIS 2 POINT/112323_Ghazal_EGTs_Standard M7_2point/"
)
twopoint.prep_plot(
    #summary_plot=True,
    save_plot=True,
    exception_files=["M8E2_2-Point.txt", "M8E3_2-Point.txt",'M8I_2-Point.txt',
                     'M8I3_2-Point.txt','M8I2_2-Point.txt','M10B_2-Point.txt'],
)

'''from two_point.two_points_copy import DiodeMeas

twopoint = DiodeMeas(
    folder_path="C:/Users/ghaza/OneDrive/Desktop/HIWI/20231114/"
)
twopoint.read_excel_file()'''
