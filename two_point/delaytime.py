import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the CSV file


def _read_data(path):
    # Read the CSV file
    df = pd.read_csv(path, sep="\t", decimal=",", thousands=None, engine="python")

    # Replace commas with dots and update scientific notation
    df = df.applymap(
        lambda x: x.replace(",", ".").replace("E", "e") if isinstance(x, str) else x
    )
    df = df.apply(pd.to_numeric, errors="coerce")

    # Rename the columns to lowercase
    df.columns = ["Time", "vin1", "vin2", "vout"]

    return df


def _find_min_max_points(df: pd.DataFrame):

    resutls = {}
    for voltage in ["vout", "vin1", "vin2"]:

        v_min = df[voltage].min()
        v_max = df[voltage].max()
        # Define smaller thresholds
        threshold_min = 0.27 * (v_max - v_min)
        threshold_max = 0.27 * (v_max - v_min)

        # Filter data within a threshold around min and max values
        within_min_threshold = df[
            (df[voltage] >= v_min) & (df[voltage] <= v_min + threshold_min)
        ]
        within_max_threshold = df[
            (df[voltage] >= v_max - threshold_max) & (df[voltage] <= v_max)
        ]
        # plot the min and max points on the same plot as the raw data
        plt.figure(figsize=(10, 6))
        plt.plot(df["Time"], df[voltage], color="gray", label="Raw Data")
        plt.scatter(
            within_min_threshold["Time"],
            within_min_threshold[voltage],
            color="red",
            label="Min Points",
        )
        plt.scatter(
            within_max_threshold["Time"],
            within_max_threshold[voltage],
            color="blue",
            label="Max Points",
        )
        plt.xlabel("Time")
        plt.ylabel(voltage)
        plt.title(f"{voltage} vs Time")
        plt.grid(True)
        plt.legend()
        # plt.show()
        resutls[voltage] = (within_min_threshold, within_max_threshold)
    #plt.show()
    return resutls


def find_gap_indices(df, threshold: float = 0.1):
    # Sort the DataFrame by the 'Time' column
    df_sorted = df.sort_values(by="Time")
    # Calculate the difference between consecutive time values
    time_diff = df_sorted["Time"].diff()
    # Find the index where the gap occurs (difference is larger than a threshold)
    gap_indices = time_diff[time_diff > threshold].index
    gap_times = df_sorted.loc[gap_indices, "Time"]
    return gap_indices, gap_times


def _find_interpolation_points(
    df,
    voltage,
    start_index_min,
    gap_indices_min,
    gap_times_min,
    vout_within_min_threshold,
    gap_indices_max,
    gap_times_max,
    vout_within_max_threshold,
    calc="50%",
):
    # Find the average vout value between the gaps
    if voltage == "vout":
        min_index = 1
        max_index = 2
    else:
        min_index = start_index_min
        max_index = 1
    # print("Min index:", min_index)
    min_second_gap_time = gap_times_min.iloc[min_index]
    # print("Second min gap time:", min_second_gap_time)
    max_second_gap_time = gap_times_max.iloc[max_index]
    # print("Second max gap time:", max_second_gap_time)
    selected_min_data = vout_within_min_threshold[
        (vout_within_min_threshold["Time"] < gap_times_min.iloc[min_index + 1])
        & (vout_within_min_threshold["Time"] > gap_times_min.iloc[min_index])
    ]
    # print("Selected min data:", selected_min_data)
    min_avg = selected_min_data[voltage].mean()
    # print("Min average:", min_avg)
    selected_max_data = vout_within_max_threshold[
        (vout_within_max_threshold["Time"] < gap_times_max.iloc[max_index + 1])
        & (vout_within_max_threshold["Time"] > gap_times_max.iloc[max_index])
    ]
    # print("Selected max data:", selected_max_data)
    if gap_times_max.iloc[max_index] > gap_times_min.iloc[min_index]:
        status = "rise"
    else:
        status = "fall"
    max_avg = selected_max_data[voltage].mean()
    # print("Max average:", max_avg)
    if calc == "50%":
        total_avg = (min_avg + max_avg) / 2
    if calc == "80%":
        total_avg = abs(min_avg - max_avg) * 0.8 + min_avg
    if calc == "20%":
        total_avg = abs(min_avg - max_avg) * 0.2 + min_avg
    # print("Total average:", total_avg)
    # Plot the rest with different color
    other_indices = df.index.difference(
        vout_within_min_threshold.index.union(vout_within_max_threshold.index)
    )
    # print("Other indices:", df.loc[other_indices])
    other_indices_data = df.loc[other_indices]
    # print("Other indices data:", other_indices_data["Time"])
    # print th other indices time is between the second min gap time and the second max gap time
    selected_points = other_indices_data[
        (other_indices_data["Time"] > min_second_gap_time)
        & (other_indices_data["Time"] < max_second_gap_time)
    ]
    if selected_points.empty:
        selected_points = other_indices_data[
            (other_indices_data["Time"] < min_second_gap_time)
            & (other_indices_data["Time"] > max_second_gap_time)
        ]
    return (
        selected_points,
        total_avg,
        other_indices,
        status,
        selected_min_data,
        selected_max_data,
        min_second_gap_time,
        max_second_gap_time,
    )


def _fit_line(
    selected_points, voltage, total_avg, selected_min_data, selected_max_data
):
    # fit a line to the vout values of the selected points and save parameters for further use
    # y = mx + c
    # m = (nΣxy - ΣxΣy) / (nΣx^2 - (Σx)^2)
    # c = (Σy - mΣx) / n
    n = len(selected_points)
    x = selected_points["Time"]
    y = selected_points[voltage]
    m = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (
        n * np.sum(x**2) - (np.sum(x)) ** 2
    )
    c = (np.sum(y) - m * np.sum(x)) / n
    total_avg_time = (total_avg - c) / m
    if np.isnan(total_avg_time):
        total_avg_time = max(
            [selected_min_data["Time"].min(), selected_max_data["Time"].min()]
        )
    return m, c, total_avg_time


path = "C:/Users/ghaza/OneDrive/Desktop/thesis/repo/TwoPointMeasurement/data/NAND2I_transient_1,0V.dat"
df = _read_data(path)
results = _find_min_max_points(df)
for voltage in ["vout", "vin1", "vin2"]:
    vout_within_min_threshold, vout_within_max_threshold = results[voltage]
    gap_indices_min, gap_times_min = find_gap_indices(vout_within_min_threshold)
    gap_indices_max, gap_times_max = find_gap_indices(vout_within_max_threshold)
    # print(f"Gap indices for min {voltage} points: {gap_indices_min}")
    # print(f"Gap times for min {voltage} points: {gap_times_min}")
    # print(f"Gap indices for max {voltage} points: {gap_indices_max}")
    # print(f"Gap times for max {voltage} points: {gap_times_max}")
    if voltage == "vout":
        min_index = 1
        for max_index in [0, 1]:
            min_second_gap_time = gap_times_min.iloc[min_index]
            max_second_gap_time = gap_times_max.iloc[max_index]
            if max_index == 0:
                ref_point1 = min_second_gap_time
            elif max_index == 1:
                ref_point2 = max_second_gap_time
            # print("Second min gap time:", min_second_gap_time)
            # print("Second max gap time:", max_second_gap_time)
            try:
                selected_min_data = vout_within_min_threshold[
                    (vout_within_min_threshold["Time"] < gap_times_min.iloc[min_index + 1])
                    & (vout_within_min_threshold["Time"] > gap_times_min.iloc[min_index])
                ]
            except:
                selected_min_data = vout_within_min_threshold[
                    (vout_within_min_threshold["Time"] < gap_times_min.iloc[min_index]+0.011)
                    & (vout_within_min_threshold["Time"] > gap_times_min.iloc[min_index])
                ]
            # print("Selected min data:", selected_min_data)
            min_avg = selected_min_data[voltage].mean()
            try:
                selected_max_data = vout_within_max_threshold[
                    (vout_within_max_threshold["Time"] < gap_times_max.iloc[max_index + 1])
                    & (vout_within_max_threshold["Time"] > gap_times_max.iloc[max_index])
                ]
            except:
                selected_max_data = vout_within_max_threshold[
                    (vout_within_max_threshold["Time"] < gap_times_max.iloc[max_index]+0.011)
                    & (vout_within_max_threshold["Time"] > gap_times_max.iloc[max_index])
                ]
            # print("Selected max data:", selected_max_data)
            max_avg = selected_max_data[voltage].mean()
            calc = "50%"
            if calc == "50%":
                total_avg = (min_avg + max_avg) / 2
            if calc == "80%":
                total_avg = abs(min_avg - max_avg) * 0.8 + min_avg
            if calc == "20%":
                total_avg = abs(min_avg - max_avg) * 0.2 + min_avg

            other_indices = df.index.difference(
                vout_within_min_threshold.index.union(vout_within_max_threshold.index)
            )
            # print("Other indices:", df.loc[other_indices])
            other_indices_data = df.loc[other_indices]

            # plot the rest with different color
            plt.figure(figsize=(10, 6))
            plt.plot(df["Time"], df[voltage], color="gray", label="Raw Data")
            plt.scatter(
                other_indices_data["Time"],
                other_indices_data[voltage],
                color="green",
                label="Other Points",
            )
            plt.xlabel("Time")
            plt.ylabel(voltage)
            plt.title(f"{voltage} vs Time")
            plt.grid(True)
            plt.legend()
            # plt.show()
            other_indices_data = df.loc[other_indices]

            selected_points = other_indices_data[
                (other_indices_data["Time"] > min_second_gap_time)
                & (other_indices_data["Time"] < max_second_gap_time)
            ]
            if selected_points.empty:
                selected_points = other_indices_data[
                    (other_indices_data["Time"] < min_second_gap_time)
                    & (other_indices_data["Time"] > max_second_gap_time)
                ]
            m, c, total_avg_time = _fit_line(
                selected_points,
                voltage,
                total_avg,
                selected_min_data,
                selected_max_data,
            )
            if max_index == 0:
                avg1 = total_avg_time
            elif max_index == 1:
                avg2 = total_avg_time
        # print(f"ref point 1: {ref_point1}")
        # print(f"ref point 2: {ref_point2}")

    elif voltage == "vin1":
        # print("voltage:", voltage)
        min_desired_index = -1
        max_desired_index = -1
        # print(f"Gap indices for min {voltage} points: {gap_times_min.values}")
        for i, gap_time in enumerate(gap_times_min.values):
            if abs(gap_time - ref_point1) < 0.15:
                # print(f"min gap time {gap_time} is close to ref point 1 {ref_point1}")
                # save the index of the gap time that is close to the ref point
                min_desired_index = i
                print(
                    f"vin1 50% time is {gap_times_min.iloc[i]} and the avg1 time is {avg1}, the differece is {abs(gap_times_min.iloc[i] - avg1) * 1000} mS"
                )
            elif abs(gap_time - ref_point2) < 0.15:
                # print(f"min gap time {gap_time} is close to ref point 2 {ref_point2}")
                min_desired_index = i
                print(
                    f"vin1 50% time is {gap_times_min.iloc[i]} and the avg2 time is {avg2}, the differece is {abs(gap_times_min.iloc[i] - avg2) * 1000} mS"
                )
        for i, gap_time in enumerate(gap_times_max.values):
            if abs(gap_time - ref_point1) < 0.15:
                # print(f"max gap time {gap_time} is close to ref point 1 {ref_point1}")
                max_desired_index = i
                print(
                    f"vin1 50% time is {gap_times_max.iloc[i]} and the avg1 time is {avg1}, the differece is {abs(gap_times_max.iloc[i] - avg1)*1000} mS"
                )
            elif abs(gap_time - ref_point2) < 0.15:
                # print(f"max gap time {gap_time} is close to ref point 2 {ref_point2}")
                max_desired_index = i
                print(
                    f"vin1 50% time is {gap_times_max.iloc[i]} and the avg2 time is {avg2}, the differece is {abs(gap_times_max.iloc[i] - avg2)*1000} mS"
                )
        """if min_desired_index != -1:
            print(f"min desired index: {min_desired_index}")
        elif max_desired_index != -1:
            print(f"max desired index: {max_desired_index}")"""

    elif voltage == "vin2":
        # print("voltage:", voltage)
        min_desired_index = -1
        max_desired_index = -1
        # print(f"Gap indices for min {voltage} points: {gap_times_min.values}")
        for i, gap_time in enumerate(gap_times_min.values):
            if abs(gap_time - ref_point1) < 0.15:
                # print(f"min gap time {gap_time} is close to ref point 1 {ref_point1}")
                # save the index of the gap time that is close to the ref point
                min_desired_index = i
                print(
                    f"vin2 50% time is {gap_times_min.iloc[i]} and the avg1 time is {avg1}, the differece is {abs(gap_times_min.iloc[i] - avg1) * 1000} mS"
                )
            elif abs(gap_time - ref_point2) < 0.15:
                # print(f"min gap time {gap_time} is close to ref point 2 {ref_point2}")
                min_desired_index = i
                print(
                    f"vin2 50% time is {gap_times_min.iloc[i]} and the avg2 time is {avg2}, the differece is {abs(gap_times_min.iloc[i] - avg2) * 1000} mS"
                )
        for i, gap_time in enumerate(gap_times_max.values):
            if abs(gap_time - ref_point1) < 0.15:
                # print(f"max gap time {gap_time} is close to ref point 1 {ref_point1}")
                max_desired_index = i
                print(
                    f"vin2 50% time is {gap_times_max.iloc[i]} and the avg1 time is {avg1}, the differece is {abs(gap_times_max.iloc[i] - avg1)*1000} mS"
                )
            elif abs(gap_time - ref_point2) < 0.15:
                # print(f"max gap time {gap_time} is close to ref point 2 {ref_point2}")
                max_desired_index = i
                print(
                    f"vin2 50% time is {gap_times_max.iloc[i]} and the avg2 time is {avg2}, the differece is {abs(gap_times_max.iloc[i] - avg2)*1000} mS"
                )
        """if min_desired_index != -1:
            print(f"min desired index: {min_desired_index}")
        elif max_desired_index != -1:
            print(f"max desired index: {max_desired_index}")"""
