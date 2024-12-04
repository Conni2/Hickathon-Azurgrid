# Groundwater Levels Dashboard

This Streamlit app provides an interactive visualization of groundwater levels across various locations. The app supports heatmap visualizations and detailed level trends for specific stations, offering users a dynamic way to analyze data over time and space.

## Features

### 📊 **Heatmap by Date**
- **Interactive Heatmap Visualization**: Displays a heatmap of groundwater levels for a specific date.
- **Color-Coded Levels**: 
  - Higher groundwater levels are represented by darker blue.
  - Lower groundwater levels are represented by darker red.
- **Filter by Levels**:
  - Users can filter the heatmap to display only specific groundwater levels (1-5) using a multi-select dropdown.
- **Data Details**:
  - A toggleable table displays detailed data (longitude, latitude, and level) for filtered points.

### 📈 **Level Trends by Station ID**
- **Station-Level Analysis**:
  - Select a specific station by its unique ID (combination of latitude and longitude).
- **Customizable Date Range**:
  - Analyze trends for the selected station over any chosen time period.
- **Line Chart Visualization**:
  - View trends in groundwater levels (1-5) for the selected station over the specified date range.

## How to Use

1. **Heatmap by Date**:
   - Go to the **"📊 Heatmap by Date"** tab.
   - Select a date from the dropdown menu to view the groundwater levels heatmap for that day.
   - Optionally, filter the displayed levels using the **"Filter by Level"** multi-select dropdown.
   - Toggle the table to view detailed data for filtered points.
   - Zoom in/out or pan the map to explore specific areas.

2. **Level Trends by Station ID**:
   - Go to the **"📈 Level Trends by Station ID"** tab.
   - Select a station from the dropdown menu (station IDs are a combination of longitude and latitude).
   - Choose a start and end date for the analysis.
   - View the line chart to analyze the groundwater level trends for the selected station within the specified date range.

## Data Used

- **Dataset**: A pre-processed CSV file (`reduced_data.csv`) containing the following columns:
  - `formatted_measurement_date`: Measurement date (formatted as YYYY-MM-DD).
  - `piezo_station_longitude`: Longitude of the station.
  - `piezo_station_latitude`: Latitude of the station.
  - `Station_ID`: Unique station identifier (combination of latitude and longitude).
  - `piezo_groundwater_level_category`: Groundwater levels encoded numerically (1 = Very Low, 5 = Very High).

## Further Development
In January, a new tab will be added to the app featuring a machine learning model to predict groundwater levels. This enhancement aims to provide predictive insights based on historical and real-time data, allowing for proactive resource management.