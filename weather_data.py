import requests
import streamlit as st
from datetime import datetime
import pytz

def get_weather(city):
    try:
        if not city.strip():
            return {"cod": "404", "message": "Please enter a city name"}
        
        api_key = "655e85d516e32dfedf870868fd4fd6e1"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "q=" + city + "&appid=" + api_key + "&units=metric"
        response = requests.get(complete_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {"cod": "404", "message": "Failed to fetch weather data. Please try again."}

st.set_page_config(page_title="Weather Info", page_icon="🌤️", layout="wide")

# Enhanced CSS styling
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stMetric {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .weather-header {
        background: linear-gradient(120deg, #2980b9, #8e44ad);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Display local time with better styling
local_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"""
    <div style='text-align: right; color: #666; padding: 10px; 
    background-color: rgba(255,255,255,0.1); border-radius: 5px;'>
    🕒 Local Time: {local_time}
    </div>
""", unsafe_allow_html=True)

# Attractive header
st.markdown("""
    <div class='weather-header'>
        <h1 style='text-align: center;'>🌈 Weather Dashboard</h1>
        <p style='text-align: center; font-size: 1.2em;'>Real-time Weather Information</p>
    </div>
""", unsafe_allow_html=True)

city = st.text_input("🌍 Enter City Name:", placeholder="e.g., London")

if city:
    with st.spinner('Fetching weather data...'):
        weather_data = get_weather(city)
    if weather_data["cod"] != "404":
        main = weather_data["main"]
        wind = weather_data["wind"]
        weather_desc = weather_data["weather"][0]["description"]
        sys = weather_data["sys"]
        weather_icon_code = weather_data["weather"][0]["icon"]
        weather_icon_url = f"http://openweathermap.org/img/wn/{weather_icon_code}@4x.png"

        timezone_offset = weather_data.get("timezone", 0)
        city_time = datetime.utcnow().replace(tzinfo=pytz.UTC)
        city_time = city_time.astimezone(pytz.FixedOffset(timezone_offset//60))
        
        # Display weather icon and current conditions
        st.markdown(f"""
            <div style='text-align: center; margin: 20px 0;'>
            <img src='{weather_icon_url}' style='width: 150px; height: 150px;'>
            <h2 style='color: #2980b9;'>{weather_desc.capitalize()}</h2>
            </div>
            <div style='background-color: rgba(255,255,255,0.1); padding: 10px; 
            border-radius: 5px; margin-bottom: 20px;'>
            🌍 Time in {city}: {city_time.strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Temperature 🌡️", f"{main['temp']}°C")
            st.metric("Feels Like 🌡️", f"{main['feels_like']}°C")
        with col2:
            st.metric("Humidity 💧", f"{main['humidity']}%")
            st.metric("Visibility 👁️", f"{weather_data.get('visibility', 0)//1000} km")
        with col3:
            st.metric("Pressure 📊", f"{main['pressure']} hPa")
            st.metric("Cloudiness ☁️", f"{weather_data['clouds']['all']}%")
        with col4:
            st.metric("Min Temp 🌡️", f"{main['temp_min']}°C")
            st.metric("Max Temp 🌡️", f"{main['temp_max']}°C")

        # Wind and weather description in attractive boxes
        st.markdown(f"""
            <div style='display: flex; gap: 20px; margin-top: 20px;'>
            <div style='flex: 1; background-color: rgba(255,255,255,0.1); 
            padding: 20px; border-radius: 10px;'>
                <h3>🌪️ Wind Information</h3>
                <p style='font-size: 1.2em;'>Speed: {wind['speed']} m/s</p>
                <p style='font-size: 1.2em;'>Direction: {wind.get('deg', 'N/A')}°</p>
            </div>
            <div style='flex: 1; background-color: rgba(255,255,255,0.1); 
            padding: 20px; border-radius: 10px;'>
                <h3>🌥️ Weather Condition</h3>
                <p style='font-size: 1.2em;'>{weather_desc.capitalize()}</p>
            </div>
            <div style='flex: 1; background-color: rgba(255,255,255,0.1); 
            padding: 20px; border-radius: 10px;'>
                <h3>🌅 Sun Times</h3>
                <p style='font-size: 1.2em;'>Sunrise: {datetime.fromtimestamp(sys['sunrise']).strftime('%H:%M')}</p>
                <p style='font-size: 1.2em;'>Sunset: {datetime.fromtimestamp(sys['sunset']).strftime('%H:%M')}</p>
            </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.error("City Not Found! 😕")