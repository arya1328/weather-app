import requests
import streamlit as st

def get_weather(city):
    api_key = "655e85d516e32dfedf870868fd4fd6e1"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&appid=" + api_key + "&units=metric"
    response = requests.get(complete_url)
    return response.json()

st.set_page_config(page_title="Weather Info", page_icon="🌤️")
st.title("☁️ Real-time Weather Information")
st.markdown("---")

# Add CSS styling
st.markdown("""
    <style>
    .main { padding: 2rem; }
    </style>
""", unsafe_allow_html=True)

city = st.text_input("🌍 Enter City Name:", placeholder="e.g., London")

if city:
    with st.spinner('Fetching weather data...'):
        weather_data = get_weather(city)
    if weather_data["cod"] != "404":
        main = weather_data["main"]
        wind = weather_data["wind"]
        weather_desc = weather_data["weather"][0]["description"]

        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Temperature 🌡️", f"{main['temp']}°C")
            st.metric("Humidity 💧", f"{main['humidity']}%")
        
        with col2:
            st.metric("Pressure 📊", f"{main['pressure']} hPa")
        st.write(f"Wind Speed: {wind['speed']} m/s")
        st.write(f"Weather Description: {weather_desc.capitalize()}")
    else:
        st.error("City Not Found!")