from two_point.two_points import TwoPoints

twopoint = TwoPoints(
    folder_path="/Users/amini_m/Desktop/repo/twoPoint/data/112323_Ghazal_EGTs_Standard M7_2point/"
)
twopoint.prep_plot(
    seprate_plot=False,
    save_plot=True,
    exception_files=["M8E2_2-Point.txt", "M8E3_2-Point.txt"],
)