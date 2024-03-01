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
    df.columns = ["Time", "vin1", "vout"]
    return df


def _find_min_max_points(df: pd.DataFrame, voltage: str):

    vout_min = df[voltage].min()
    vout_max = df[voltage].max()

    # Define smaller thresholds
    threshold_min = 0.15 * (vout_max - vout_min)
    threshold_max = 0.15 * (vout_max - vout_min)

    # Filter data within a threshold around min and max values
    vout_within_min_threshold = df[
        (df[voltage] >= vout_min) & (df[voltage] <= vout_min + threshold_min)
    ]
    vout_within_max_threshold = df[
        (df[voltage] >= vout_max - threshold_max) & (df[voltage] <= vout_max)
    ]
    # print("Data within Min Threshold:")
    # print(vout_within_min_threshold)

    # Plot vout against time
    plt.figure(figsize=(10, 6))

    # Plot raw data line
    plt.plot(df["Time"], df[voltage], color="gray", label="Raw Data")

    # Mark individual points for different segments based on thresholding
    plt.scatter(
        vout_within_min_threshold["Time"],
        vout_within_min_threshold[voltage],
        color="red",
        label="Within Min Threshold",
        marker="o",
    )
    plt.scatter(
        vout_within_max_threshold["Time"],
        vout_within_max_threshold[voltage],
        color="green",
        label="Within Max Threshold",
        marker="o",
    )

    return vout_within_min_threshold, vout_within_max_threshold


def find_gap_indices(df, threshold: float = 0.1):
    # Sort the DataFrame by the 'Time' column
    df_sorted = df.sort_values(by="Time")
    # Calculate the difference between consecutive time values
    time_diff = df_sorted["Time"].diff()
    # Find the index where the gap occurs (difference is larger than a threshold)
    gap_indices = time_diff[time_diff > threshold].index
    gap_times = df_sorted.loc[gap_indices, "Time"]
    return gap_indices, gap_times


# print("Gap indices:", gap_indices_min)
# print("Time values at the gaps:", gap_times_min)
# print("Gap indices:", gap_indices_max)
# print("Time values at the gaps:", gap_times_max)
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
        max_index = start_index_min
    else:
        min_index = start_index_min
        max_index = 1
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


def calculate_time(df, measured_voltage, show_plot=True, calc="50%"):

    vout_within_min_threshold, vout_within_max_threshold = _find_min_max_points(
        df, voltage=measured_voltage
    )

    gap_indices_min, gap_times_min = find_gap_indices(vout_within_min_threshold)
    gap_indices_max, gap_times_max = find_gap_indices(vout_within_max_threshold)

    (
        selected_points,
        total_avg,
        other_indices,
        status1,
        selected_min_data,
        selected_max_data,
        min_second_gap_time,
        max_second_gap_time,
    ) = _find_interpolation_points(
        df,
        measured_voltage,
        1,
        gap_indices_min,
        gap_times_min,
        vout_within_min_threshold,
        gap_indices_max,
        gap_times_max,
        vout_within_max_threshold,
        calc,
    )
    m, c, total_avg_time = _fit_line(
        selected_points,
        measured_voltage,
        total_avg,
        selected_min_data,
        selected_max_data,
    )
    avg1 = total_avg_time
    occurance_time1 = max([min_second_gap_time, max_second_gap_time])
    # print(f"Total average time for {status1} at {occurance_time1}is: {total_avg_time}")

    (
        selected_points,
        total_avg,
        other_indices,
        status2,
        selected_min_data,
        selected_max_data,
        min_second_gap_time,
        max_second_gap_time,
    ) = _find_interpolation_points(
        df,
        measured_voltage,
        2,
        gap_indices_min,
        gap_times_min,
        vout_within_min_threshold,
        gap_indices_max,
        gap_times_max,
        vout_within_max_threshold,
        calc,
    )

    m, c, total_avg_time = _fit_line(
        selected_points,
        measured_voltage,
        total_avg,
        selected_min_data,
        selected_max_data,
    )
    avg2 = total_avg_time
    occurance_time2 = max([min_second_gap_time, max_second_gap_time])
    # print(f"Total average time for {status2} at {occurance_time2}is: {total_avg_time}")

    plt.scatter(
        df.loc[other_indices, "Time"],
        df.loc[other_indices, measured_voltage],
        color="blue",
        label="Other",
        marker="o",
    )

    plt.xlabel("Time")
    plt.ylabel(measured_voltage)
    plt.title(f"{measured_voltage} vs Time")
    plt.grid(True)
    plt.legend()
    if show_plot:
        plt.show()

    return avg1, status1, avg2, status2, occurance_time1, occurance_time2


def main():
    measurements = ["vout", "vin1"]
    path = "C:/Users/Hiva/Desktop/Virevo-project/TwoPointMeasurement/data/M1E_tran_VDD_1,0V.DAT"
    df = _read_data(path)
    show_plot = False
    res = {}
    for measured_voltage in measurements:
        avg1, status1, avg2, status2, occurance_time1, occurance_time2 = calculate_time(
            df, measured_voltage, show_plot
        )
        res[measured_voltage] = {
            status1: [occurance_time1, avg1],
            status2: [occurance_time2, avg2],
        }

    time_1 = abs(res["vout"]["rise"][1] - res["vin1"]["fall"][1])
    print(f"The time delay at {res['vout']['rise'][0]} is: {time_1*1e3} mS")
    time_2 = abs(res["vout"]["fall"][1] - res["vin1"]["rise"][1])
    print(f"The time delay at {res['vout']['fall'][0]} is: {time_2*1e3} mS")

    avg11, status11, avg21, status21, occurance_time11, occurance_time21 = (
        calculate_time(df, "vout", show_plot, calc="80%")
    )
    avg12, status12, avg22, status22, occurance_time12, occurance_time22 = (
        calculate_time(df, "vout", show_plot, calc="20%")
    )
    time_3 = abs(avg11 - avg12)
    print(f"The time delay of vout between 20% and 80% at {occurance_time11} is: {time_3*1e3} mS")
    time_4 = abs(avg21 - avg22)
    print(f"The time delay of vout between 20% and 80% at {occurance_time21} is: {time_4*1e3} mS")


if __name__ == "__main__":
    main()
