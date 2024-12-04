import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Streamlit 설정
st.set_page_config(page_title="Groundwater Levels Dashboard", layout="wide")

# 데이터 로드 및 캐싱
@st.cache_data
def load_data():
    # 전처리된 데이터 경로에서 파일 로드
    data = pd.read_csv('data/reduced_data.csv')
    return data

# 데이터 로드
data = load_data()

# Streamlit 제목
st.title("Groundwater Levels Dashboard")

# 탭 구성
tab1, tab2 = st.tabs(["📊 Heatmap by Date", "📈 Level Trends by Station ID"])

# 탭 1: Heatmap by Date
with tab1:
    st.header("📊 Heatmap by Date")
    unique_dates = pd.to_datetime(data['formatted_measurement_date']).dt.date.unique()
    selected_date = st.selectbox("Select a Date", sorted(unique_dates))

    # 선택한 날짜의 데이터 필터링
    filtered_data = data[pd.to_datetime(data['formatted_measurement_date']).dt.date == selected_date]

    if not filtered_data.empty:
        # 기본 히트맵
        fig = px.density_mapbox(
            filtered_data,
            lat='piezo_station_latitude',
            lon='piezo_station_longitude',
            z='piezo_groundwater_level_category',
            radius=15,  # 히트맵 크기 키우기
            color_continuous_scale=['red', 'blue'],  # 빨강-파랑 그라데이션
            title=f"Groundwater Levels Heatmap on {selected_date}",
            labels={'piezo_station_longitude': 'Longitude', 'piezo_station_latitude': 'Latitude'},
            mapbox_style="carto-positron",
            zoom=6,
            height=600  # 히트맵 높이 조정
        )
        st.plotly_chart(fig, use_container_width=True)

        # 추가 필터링 히트맵
        st.subheader("🎚 Filtered Heatmap by Levels and Date")

        # 레벨 선택
        selected_levels = st.multiselect(
            "Select Levels to Display",
            options=[1, 2, 3, 4, 5],
            default=[1, 3, 5]  # 기본 선택값
        )

        # 필터링 데이터
        filtered_by_date_and_levels = data[
            (pd.to_datetime(data['formatted_measurement_date']).dt.date == selected_date) &
            (data['piezo_groundwater_level_category'].isin(selected_levels))
        ]

        if not filtered_by_date_and_levels.empty:
            # 히트맵 생성
            fig_filtered = px.density_mapbox(
                filtered_by_date_and_levels,
                lat='piezo_station_latitude',
                lon='piezo_station_longitude',
                z='piezo_groundwater_level_category',
                radius=15,
                color_continuous_scale=["blue", "red"],  # 파란색~빨간색
                title=f"Filtered Heatmap for Levels {selected_levels} on {selected_date}",
                labels={'piezo_station_longitude': 'Longitude', 'piezo_station_latitude': 'Latitude'},
                mapbox_style="carto-positron",
                zoom=6,
                height=600
            )
            st.plotly_chart(fig_filtered, use_container_width=True)

            # 토글 버튼으로 데이터 표 보기
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



# 탭 2: Level Trends by Station ID
with tab2:
    st.header("📈 Level Trends by Station ID")
    st.markdown("""
    **Station ID** is a combination of the station's longitude and latitude. For example, 
    a station with longitude `2.349014` and latitude `48.864716` will have a Station ID of `2.349014_48.864716`.
    """)

    # Station ID 선택
    unique_stations = data['Station_ID'].unique()
    selected_station = st.selectbox("Select a Station ID", unique_stations)
    
    # 날짜 범위 선택
    start_date = st.date_input("Start Date", value=datetime(2020, 5, 1).date())
    end_date = st.date_input("End Date", value=datetime(2020, 9, 30).date())

    # 선택된 Station ID에 해당하는 데이터 필터링
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
