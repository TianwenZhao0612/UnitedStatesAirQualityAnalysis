# United States Air Quality Analysis 🌍

## Description
This project provides **interactive visualizations** for analyzing **air quality trends across the United States**. The analysis focuses on key pollutants from 2000 to 2016, using officially released data from the **United States Environmental Protection Agency (EPA)**.  

### Visualizations Included:

### 1. Choropleth Map:  
- Displays the **average air quality index (AQI)** for different pollutants (NO2, O3, SO2, CO) across all US states.
- Users can **select pollutants** from a dropdown menu.
- **Color gradient** helps quickly identify states with high pollution levels.

### 2. Time Series Line Chart:  
- Shows **daily average pollutant levels** from 2000 to 2016.
- Users can select different pollutants to explore historical trends.
- The x-axis represents time (Date Local), and the y-axis displays pollutant concentrations.

### 3. State-wise Bar Chart:  
- Ranks states based on their **average NO2 levels** over the full time period.
- The bars are **color-coded** to reflect pollution severity (red = high, green = low).
- This chart helps quickly compare air quality across states.

---

## Installation
To install necessary dependencies, run the following commands:
pip install pandas==2.2.0
pip install numpy==1.26.4
pip install streamlit==1.32.0
pip install plotly==5.18.0
pip install geopandas==0.14.3
pip install matplotlib==3.8.2


---

## Usage
### Option 1: Online Deployment (Recommended)  
Visit the deployed Streamlit app at:  
[https://your-username-your-repo-name.streamlit.app](https://www.streamlit.io)  
(Note: Replace the link with your actual deployment link)

### Option 2: Local Run  
Clone this repository and run the app locally:

git clone https://github.com/TianwenZhao0612/UnitedStatesAirQualityAnalysis.git
cd UnitedStatesAirQualityAnalysis
streamlit run finalproject.py

---

## Data Source
This project uses publicly available air quality data provided by the **United States Environmental Protection Agency (EPA)**.  
Dataset: `pollution_us_2000_2016.csv`  
Source: [https://www.kaggle.com/datasets/sogun3/uspollution](https://www.kaggle.com/datasets/sogun3/uspollution)


