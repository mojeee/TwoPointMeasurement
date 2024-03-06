import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from scipy.interpolate import make_interp_spline
import numpy as np
from sklearn.linear_model import LinearRegression


uploaded_file = st.file_uploader("Upload a .dat file", type="dat")

if uploaded_file is not None:
    df = pd.read_csv(
        uploaded_file, sep="\t", decimal=",", thousands=None, engine="python"
    )

    df = df.applymap(
        lambda x: x.replace(",", ".").replace("E", "e") if isinstance(x, str) else x
    )
    df = df.apply(pd.to_numeric, errors="coerce")

    try:
        df.columns = ["Time", "vin1", "vout"]
    except:
        df.columns = ["Time", "vin1", "vin2", "vout"]

    st.write(f"File is uploaded successfully!")
    #st.write(df.head(5))

    if len(df.columns) == 3:
        fig1 = go.Figure()
        fig1.add_trace(
            go.Scatter(x=df["Time"], y=df["vin1"], mode="lines", name="Vin1")
        )
        fig1.update_layout(
            title_text="Time vs Vin1",
            title_x=0.5,
            xaxis_title="Time",
            yaxis_title="Voltage",
        )
        fig1.update_layout(showlegend=True)
        st.plotly_chart(fig1)

        fig2 = go.Figure()
        fig2.add_trace(
            go.Scatter(x=df["Time"], y=df["vout"], mode="lines", name="Vout")
        )
        fig2.update_layout(
            title_text="Time vs Vout",
            title_x=0.5,
            xaxis_title="Time",
            yaxis_title="Voltage",
        )
        fig2.update_layout(showlegend=True)
        st.plotly_chart(fig2)

        threshold = float(
            (
                st.number_input(
                    "Insert a threshold value for noise in percent", value=0.0, step=0.1
                )
            )
            / 100
        )
        vout_starting_value = float(
            st.number_input(
                "Insert an estimation for the starting value of Vout",
                value=0.0,
                step=0.1,
            )
        )

    elif len(df.columns) == 4:
        fig1 = go.Figure()
        fig1.add_trace(
            go.Scatter(x=df["Time"], y=df["vin1"], mode="lines", name="Vin1")
        )
        fig1.update_layout(
            title_text="Time vs Vin1",
            title_x=0.5,
            xaxis_title="Time",
            yaxis_title="Voltage",
        )
        fig1.update_layout(showlegend=True)
        st.plotly_chart(fig1)

        fig3 = go.Figure()
        fig3.add_trace(
            go.Scatter(x=df["Time"], y=df["vin2"], mode="lines", name="Vin2")
        )
        fig3.update_layout(
            title_text="Time vs Vin2",
            title_x=0.5,
            xaxis_title="Time",
            yaxis_title="Voltage",
        )
        fig3.update_layout(showlegend=True)
        st.plotly_chart(fig3)

        fig2 = go.Figure()
        fig2.add_trace(
            go.Scatter(x=df["Time"], y=df["vout"], mode="lines", name="Vout")
        )
        fig2.update_layout(
            title_text="Time vs Vout",
            title_x=0.5,
            xaxis_title="Time",
            yaxis_title="Voltage",
        )
        fig2.update_layout(showlegend=True)
        st.plotly_chart(fig2)
        threshold = float(
            (
                st.sidebar.number_input(
                    "Insert a threshold value for noise in percent", value=0.0, step=0.1
                )
            )
            / 100
        )
        first_period_start = float(
            st.sidebar.number_input(
                "Insert the starting value of the first period of jump",
                value=0.0,
                step=0.1,
            )
        )
        first_period_end = float(
            st.sidebar.number_input(
                "Insert the ending value of the first period of jump",
                value=0.0,
                step=0.1,
            )
        )
        second_period_start = float(
            st.sidebar.number_input(
                "Insert the starting value of the second period of jump",
                value=0.0,
                step=0.1,
            )
        )
        second_period_end = float(
            st.sidebar.number_input(
                "Insert the ending value of the second period of jump",
                value=0.0,
                step=0.1,
            )
        )

        df_first = df[
            (df["Time"] >= first_period_start) & (df["Time"] <= first_period_end)
        ]

        df_second = df[
            (df["Time"] >= second_period_start) & (df["Time"] <= second_period_end)
        ]

        for i, value in enumerate(df_first["vout"]):
            if (
                i != 0
                and abs(df_first["vout"].iloc[i] - df_first["vout"].iloc[i - 1])
                > threshold
            ):
                jump_index_1 = i
                break

        x_data = df_first["Time"][jump_index_1 - 3 : jump_index_1 + 3]
        y_data = df_first["vout"][jump_index_1 - 3 : jump_index_1 + 3]

        # Interpolate the data with a spline
        spline = make_interp_spline(x_data, y_data, k=1)  # k=3 specifies cubic spline
        x_spline = np.linspace(min(x_data), max(x_data), 1000)
        y_spline = spline(x_spline)

        # Assuming 'x_value' is the x-coordinate where you want to predict the corresponding y-value
        # 'spline' is the spline function obtained from make_interp_spline
        # after_jump = df_first["vout"][jump_index:].mean()
        m = (y_data.iloc[2] - y_data.iloc[3]) / (x_data.iloc[2] - x_data.iloc[3])
        b = y_data.iloc[2] - m * x_data.iloc[2]

        # Assuming 'x_value' is the x-coordinate where you want to predict the corresponding y-value
        # 'spline' is the spline function obtained from make_interp_spline
        y_value_1 = df_first["vout"][jump_index_1 - 3 : jump_index_1 + 3].mean()
        y_value_1_max = df_first["vout"][jump_index_1 - 3 : jump_index_1 + 3].max()
        y_value_1_min = df_first["vout"][jump_index_1 - 3 : jump_index_1 + 3].min()
        y_value_1_at_20_pecent = y_value_1_min + 0.2 * (y_value_1_max - y_value_1_min)
        y_value_1_at_80_pecent = y_value_1_min + 0.8 * (y_value_1_max - y_value_1_min)
        predicted_x_20 = (y_value_1_at_20_pecent - b) / m
        predicted_x_80 = (y_value_1_at_80_pecent - b) / m
        predicted_x_1 = (y_value_1 - b) / m

        #st.write(f"Predicted x value at 50%: {predicted_x_1}")
        #st.write(f"Predicted x value at 20%: {predicted_x_20}")
        #st.write(f"Predicted x value at 80%: {predicted_x_80}")
        # Plotting the original data and spline along with the predicted point
        df_selected = df[
            (df["Time"] >= (predicted_x_1 - 0.1))
            & (df["Time"] <= (predicted_x_1 + 0.1))
        ]

        jump_index_12 = 0
        for i, value in enumerate(df_selected["vin1"]):
            if (
                i != 0
                and abs(df_selected["vin1"].iloc[i] - df_selected["vin1"].iloc[i - 1])
                > threshold
            ):
                jump_index_12 = i
                break
        if jump_index_12 == 0:
            for i,value in enumerate(df_selected["vin2"]):
                if (
                    i != 0
                    and abs(df_selected["vin2"].iloc[i] - df_selected["vin2"].iloc[i - 1])
                    > threshold
                ):
                    jump_index_12 = i
                    break

        #st.write(f'Jump index 1: {df_selected["Time"].iloc[jump_index_12]}')
        st.write(
            f'time delay is: {abs(predicted_x_1 - df_selected["Time"].iloc[jump_index_12])*1000} mS'
        )
        st.write(f"Predicted x value between 20% - 80%: {abs(predicted_x_80 - predicted_x_20)*1000} mS")

        # Plotting the original data and spline along with the predicted point
        fig = go.Figure()

        # Plot the original data points
        fig.add_trace(
            go.Scatter(
                x=df_first["Time"][jump_index_1 - 3 : jump_index_1 + 3],
                y=df_first["vout"][jump_index_1 - 3 : jump_index_1 + 3],
                mode="markers",
                name="Vout around the jump",
            )
        )

        # Plot the spline
        fig.add_trace(
            go.Scatter(x=x_spline, y=y_spline, mode="lines", name="Spline Fit")
        )

        # Plot the predicted point
        fig.add_trace(
            go.Scatter(
                x=[predicted_x_1],
                y=[y_value_1],
                mode="markers",
                name="Predicted Point",
                marker=dict(color="red", size=10),
            )
        )

        fig.update_layout(
            title_text="Spline Fit with Predicted Point",
            title_x=0.5,
            xaxis_title="Time",
            yaxis_title="Voltage",
        )
        fig.update_layout(showlegend=True)

        st.plotly_chart(fig)

        for i, value in enumerate(df_second["vout"]):
            if (
                i != 0
                and abs(df_second["vout"].iloc[i] - df_second["vout"].iloc[i - 1])
                > threshold
            ):
                jump_index_2 = i
                break

        x_data = df_second["Time"][jump_index_2 - 3 : jump_index_2 + 3]
        y_data = df_second["vout"][jump_index_2 - 3 : jump_index_2 + 3]
        # st.write(x_data.iloc[2])
        # st.write(y_data.iloc[2])
        spline = make_interp_spline(x_data, y_data, k=1)  # k=3 specifies cubic spline
        x_spline = np.linspace(min(x_data), max(x_data), 1000)
        y_spline = spline(x_spline)
        m = (y_data.iloc[2] - y_data.iloc[3]) / (x_data.iloc[2] - x_data.iloc[3])
        b = y_data.iloc[2] - m * x_data.iloc[2]

        # Assuming 'x_value' is the x-coordinate where you want to predict the corresponding y-value
        # 'spline' is the spline function obtained from make_interp_spline
        y_value_2 = df_second["vout"][jump_index_2 - 3 : jump_index_2 + 3].mean()
        y_value_2_max = df_second["vout"][jump_index_2 - 3 : jump_index_2 + 3].max()
        y_value_2_min = df_second["vout"][jump_index_2 - 3 : jump_index_2 + 3].min()
        y_value_2_at_20_pecent = y_value_2_min + 0.2 * (y_value_2_max - y_value_2_min)
        y_value_2_at_80_pecent = y_value_2_min + 0.8 * (y_value_2_max - y_value_2_min)
        predicted_x_20 = (y_value_2_at_20_pecent - b) / m
        predicted_x_80 = (y_value_2_at_80_pecent - b) / m

        predicted_x_2 = (y_value_2 - b) / m
        #st.write(f"Predicted x value: {predicted_x_2}")
        #st.write(f"Predicted x value at 20%: {predicted_x_20}")
        #st.write(f"Predicted x value at 80%: {predicted_x_80}")
        # Plotting the original data and spline along with the predicted point
        df_selected = df[
            (df["Time"] >= (predicted_x_2 - 0.1))
            & (df["Time"] <= (predicted_x_2 + 0.1))
        ]

        jump_index_22 = 0
        for i, value in enumerate(df_selected["vin1"]):
            if (
                i != 0
                and abs(df_selected["vin1"].iloc[i] - df_selected["vin1"].iloc[i - 1])
                > threshold
            ):
                jump_index_22 = i
                break
        if jump_index_22 == 0:
            for i,value in enumerate(df_selected["vin2"]):
                if (
                    i != 0
                    and abs(df_selected["vin2"].iloc[i] - df_selected["vin2"].iloc[i - 1])
                    > threshold
                ):
                    jump_index_22 = i
                    break

        #st.write(f'Jump index 1: {df_selected["Time"].iloc[jump_index_22]}')
        st.write(
            f'time delay is: {abs(predicted_x_2 - df_selected["Time"].iloc[jump_index_22])*1000} mS'
        )
        st.write(f"Predicted x value between 20% - 80%: {abs(predicted_x_80 - predicted_x_20)*1000} mS")

        fig = go.Figure()

        # Plot the original data points
        fig.add_trace(
            go.Scatter(
                x=df_second["Time"][jump_index_2 - 3 : jump_index_2 + 3],
                y=df_second["vout"][jump_index_2 - 3 : jump_index_2 + 3],
                mode="markers",
                name="Vout around the jump",
            )
        )

        # Plot the spline
        fig.add_trace(
            go.Scatter(x=x_spline, y=y_spline, mode="lines", name="Spline Fit")
        )

        # Plot the predicted point
        fig.add_trace(
            go.Scatter(
                x=[predicted_x_2],
                y=[y_value_2],
                mode="markers",
                name="Predicted Point",
                marker=dict(color="red", size=10),
            )
        )

        fig.update_layout(
            title_text="Spline Fit with Predicted Point",
            title_x=0.5,
            xaxis_title="Time",
            yaxis_title="Voltage",
        )
        fig.update_layout(showlegend=True)

        st.plotly_chart(fig)
