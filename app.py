import streamlit as st
import pandas as pd
import plotly.express as px
import gdown
from datetime import datetime

# Streamlit settings
st.set_page_config(page_title="Groundwater Levels Dashboard", layout="wide")

# Load data from Google Drive
@st.cache_data
def load_data():
    # Google Drive file ID and download URL
    file_id = "1YviC8s1rdIWKM-1XPacpbbUH4fllVYPi"
    url = f"https://drive.google.com/uc?id={file_id}"

    # Download the file
    output = "reduced_data.csv"
    gdown.download(url, output, quiet=False)

    # Load the data into a DataFrame
    data = pd.read_csv(output)
    return data

# Load the data
data = load_data()

# Streamlit title
st.title("Groundwater Levels Dashboard")

# Tab configuration
tab1, tab2 = st.tabs(["📊 Heatmap by Date", "📈 Level Trends by Station ID"])

# Tab 1: Heatmap by Date
with tab1:
    st.header("📊 Heatmap by Date")
    unique_dates = pd.to_datetime(data['formatted_measurement_date']).dt.date.unique()
    selected_date = st.selectbox("Select a Date", sorted(unique_dates))

    # Filter data for the selected date
    filtered_data = data[pd.to_datetime(data['formatted_measurement_date']).dt.date == selected_date]

    if not filtered_data.empty:
        # Main heatmap
        fig = px.density_mapbox(
            filtered_data,
            lat='piezo_station_latitude',
            lon='piezo_station_longitude',
            z='piezo_groundwater_level_category',
            radius=15,  # Increase heatmap size
            color_continuous_scale=['red', 'blue'],  # Red-Blue gradient
            title=f"Groundwater Levels Heatmap on {selected_date}",
            labels={'piezo_station_longitude': 'Longitude', 'piezo_station_latitude': 'Latitude'},
            mapbox_style="carto-positron",
            zoom=6,
            height=600  # Adjust heatmap height
        )
        st.plotly_chart(fig, use_container_width=True)

        # Additional filtered heatmap
        st.subheader("🎚 Filtered Heatmap by Levels and Date")
        selected_levels = st.multiselect(
            "Select Levels to Display",
            options=[1, 2, 3, 4, 5],
            default=[1, 3, 5]
        )
        filtered_by_date_and_levels = data[
            (pd.to_datetime(data['formatted_measurement_date']).dt.date == selected_date) &
            (data['piezo_groundwater_level_category'].isin(selected_levels))
        ]

        if not filtered_by_date_and_levels.empty:
            fig_filtered = px.density_mapbox(
                filtered_by_date_and_levels,
                lat='piezo_station_latitude',
                lon='piezo_station_longitude',
                z='piezo_groundwater_level_category',
                radius=15,
                color_continuous_scale=["blue", "red"],  # Blue-Red gradient
                title=f"Filtered Heatmap for Levels {selected_levels} on {selected_date}",
                labels={'piezo_station_longitude': 'Longitude', 'piezo_station_latitude': 'Latitude'},
                mapbox_style="carto-positron",
                zoom=6,
                height=600
            )
            st.plotly_chart(fig_filtered, use_container_width=True)

            with st.expander("View Filtered Data Table"):
                st.dataframe(
                    filtered_by_date_and_levels[['piezo_groundwater_level_category', 
                                                 'piezo_station_longitude', 
                                                 'piezo_station_latitude']].rename(
                        columns={
                            'piezo_groundwater_level_category': 'Level',
                            'piezo_station_longitude': 'Longitude',
                            'piezo_station_latitude': 'Latitude'
                        }
                    )
                )
        else:
            st.warning(f"No data available for levels {selected_levels} on the selected date.")

# Tab 2: Level Trends by Station ID
with tab2:
    st.header("📈 Level Trends by Station ID")
    st.markdown("""
    **Station ID** is a combination of the station's longitude and latitude. For example, 
    a station with longitude `2.349014` and latitude `48.864716` will have a Station ID of `2.349014_48.864716`.
    """)

    unique_stations = data['Station_ID'].unique()
    selected_station = st.selectbox("Select a Station ID", unique_stations)

    start_date = st.date_input("Start Date", value=datetime(2020, 5, 1).date())
    end_date = st.date_input("End Date", value=datetime(2020, 9, 30).date())

    station_data = data[
        (data['Station_ID'] == selected_station) &
        (pd.to_datetime(data['formatted_measurement_date']).dt.date >= start_date) &
        (pd.to_datetime(data['formatted_measurement_date']).dt.date <= end_date)
    ]

    if not station_data.empty:
        fig = px.line(
            station_data,
            x='formatted_measurement_date',
            y='piezo_groundwater_level_category',
            title=f"Level Trends for Station {selected_station}",
            labels={
                'formatted_measurement_date': 'Date',
                'piezo_groundwater_level_category': 'Groundwater Level (1-5)'
            },
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected station and date range.")
