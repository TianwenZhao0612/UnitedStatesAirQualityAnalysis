import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="US Air Quality Dashboard", page_icon="🇺🇸", layout="wide")

# Title and intro
st.markdown("# 🇺🇸 United States Air Quality Analysis")
st.write("This interactive dashboard analyzes air pollution across the United States, focusing on **NO₂ AQI**.")
st.markdown("---")

# Sidebar - Data Upload
st.sidebar.markdown("## 🎛️ Data Selection & Filters")
uploaded_file = st.sidebar.file_uploader("Upload Air Quality Data (CSV)", type=["csv"])

# Load data - 优先上传文件，否则用本地
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ Data uploaded successfully!")
else:
    df = pd.read_csv('pollution_us_2000_2016.csv')
    st.sidebar.info("Using local file: pollution_us_2000_2016.csv")

# Remove non-US data
df = df[df['State'] != 'Country Of Mexico']

# State name to abbreviation mapping
state_name_to_abbr = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'District Of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI',
    'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME',
    'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
    'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE',
    'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
    'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI',
    'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
    'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}
df['State Abbr'] = df['State'].map(state_name_to_abbr)

# Average AQI per state
state_avg_aqi = df.groupby('State Abbr')['NO2 AQI'].mean().reset_index()

# Find most and least polluted
most_polluted = state_avg_aqi.loc[state_avg_aqi['NO2 AQI'].idxmax()]
least_polluted = state_avg_aqi.loc[state_avg_aqi['NO2 AQI'].idxmin()]

most_polluted_state = most_polluted['State Abbr']
highest_aqi = most_polluted['NO2 AQI']

least_polluted_state = least_polluted['State Abbr']
lowest_aqi = least_polluted['NO2 AQI']

# Map + Analysis Summary
st.markdown("### 🗺️ Air Quality Map")

col1, col2 = st.columns([3, 2])

with col1:
    fig = px.choropleth(state_avg_aqi,
                        locations='State Abbr',
                        locationmode='USA-states',
                        color='NO2 AQI',
                        scope="usa",
                        color_continuous_scale=[(0, "green"), (0.5, "yellow"), (1, "red")],
                        title="Air Quality by State (NO₂ AQI)")
    st.plotly_chart(fig)

with col2:
    st.markdown(f"""
    ### Analysis Summary
    - 🟢 Green = Clean air, low NO₂ pollution
    - 🟡 Yellow = Moderate air quality
    - 🔴 Red = Heavy NO₂ pollution, poor air quality
    ---
    - 🏭 The state with the **worst air quality**: **{most_polluted_state}**  
      ⏺️ Average NO₂ AQI: **{highest_aqi:.2f}**
    - 🌿 The state with the **best air quality**: **{least_polluted_state}**  
      ⏺️ Average NO₂ AQI: **{lowest_aqi:.2f}**
    ---
    ### Why Air Quality Differs Across States
    | Factor | Explanation |
    |---|---|
    | **Population Density** | Urban areas with more traffic and industry tend to have higher pollution. |
    | **Industrial Emissions** | States with heavy industry show worse air quality. |
    | **Traffic Pollution** | High vehicle emissions contribute significantly to NO₂ levels. |
    | **Weather & Geography** | Wind, temperature, and terrain influence pollution dispersion. |
    | **Environmental Policies** | States with stricter regulations usually have cleaner air. |
    """)

st.markdown("---")

# Time Series Trend Analysis
st.markdown("### 📈 Air Pollution Trends Over Time")

st.markdown("""
This line chart illustrates the **daily average concentration** of the selected pollutant across the United States.  
It helps visualize **long-term trends**, **seasonal patterns**, and **potential pollution spikes** over time.

### What Do These Pollutants Mean?
| Pollutant | Explanation |
|---|---|
| **NO₂ (Nitrogen Dioxide)** | Emitted mainly from vehicles, power plants, and industrial facilities. High levels can cause respiratory problems. |
| **O₃ (Ozone)** | A secondary pollutant formed when sunlight reacts with pollutants like NO₂ and VOCs. High levels can trigger asthma attacks. |
| **SO₂ (Sulfur Dioxide)** | Released from burning fossil fuels (coal & oil). Can cause respiratory irritation and contribute to acid rain. |
| **CO (Carbon Monoxide)** | Produced from incomplete combustion of fuels. Dangerous at high concentrations as it reduces oxygen delivery in the body. |
""")

df['Date Local'] = pd.to_datetime(df['Date Local'])
pollutant_options = ['NO2 Mean', 'O3 Mean', 'SO2 Mean', 'CO Mean']
selected_pollutant = st.selectbox("Select Pollutant to Display", pollutant_options)

trend_data = df.groupby('Date Local')[selected_pollutant].mean().reset_index()

fig_trend = px.line(trend_data, x='Date Local', y=selected_pollutant,
                    title=f'{selected_pollutant} Daily Trend')
st.plotly_chart(fig_trend)



st.markdown("""
### How to Read This Chart
- **Spikes** indicate days with particularly high pollution.
- **Seasonal Cycles** may suggest weather-related pollution patterns (e.g., more NO₂ in winter due to heating emissions).
- **Long-Term Trend** can show whether air quality is improving or worsening over the years.
""")

st.markdown("---")

# Bar Chart - State Ranking

st.markdown("### 📊 State-wise Average NO₂ AQI")

fig_bar = px.bar(state_avg_aqi.sort_values('NO2 AQI', ascending=False),
                 x='State Abbr', y='NO2 AQI',
                 color='NO2 AQI', color_continuous_scale=[(0, "green"), (0.5, "yellow"), (1, "red")],
                 title="Average NO₂ AQI by State")
fig_bar.update_layout(xaxis_tickangle=0)

st.plotly_chart(fig_bar)


st.markdown("""
This **ranking chart** shows how each US state performs in terms of **average NO₂ pollution**.

### What does this chart tell us?
- 🥇 The states at the **top** (e.g., Arizona, Colorado) suffer from **higher pollution levels**, meaning residents may experience:
    - More respiratory problems (asthma, coughing)
    - Hazy skies and reduced visibility
    - Potential environmental impacts (e.g., acid rain)

- 🥦 The states at the **bottom** (e.g., South Carolina, Tennessee) enjoy **better air quality**, meaning:
    - Cleaner air for outdoor activities
    - Lower health risks related to nitrogen dioxide
    - More sustainable living environment

---

### Why does air quality vary so much?
| Factor | Influence on NO₂ Pollution |
|---|---|
| 🚗 Traffic & Vehicles | More cars = more NO₂ emissions |
| 🏭 Industrial Activity | Heavy industry releases large amounts of pollutants |
| 🌍 Geography & Climate | Natural airflow can trap or disperse pollution |
| 📜 Environmental Policies | Stricter rules = cleaner air |
""")

