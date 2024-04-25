import datetime
import streamlit as st
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData

data_manager = DataManager()
flight_search = FlightSearch()
flight_data = FlightData()

with open("static/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

st.title("Fly Me To the Mean")

st.header("Helping you plan your international meetup since 2024.")
st.image("static/glass_onion_blanc_boarding.jpg")


with st.form("my_form"):
    with st.sidebar:
        st.write("From where, and when, would you and your friends like to travel?")

        travelling_from = st.text_input(
            label=":airplane: We are travelling from (e.g.: Paris, Berlin)"
        )
        from_date = st.date_input(":luggage: Earliest travel date")
        to_date = st.date_input(":house: Latest return date")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")

if submitted:
    with st.spinner(":sleuth_or_spy: Getting your best flights..."):
        st.write("Please enjoy to some music while you wait!")
        st.audio(
            "static/Fly Me To The Moon _Remastered_.mp3",
            format="audio/mp3",
            start_time=0,
            sample_rate=None,
            end_time=None,
            loop=False,
        )
        departure_cities = [
            {"city": city.strip()} for city in travelling_from.split(",")
        ]
        departure_cities = flight_search.get_city_id(departure_cities)
        all_flights = flight_search.get_cheap_flights(departure_cities)
        shared_destination_flights = flight_data.filter_by_shared_destinations(
            all_flights
        )
        best_flights_df = flight_data.structure_flight_data(
            shared_destination_flights
        )
        st.write(f"Travelling from {travelling_from}...")
        st.write(":bulb: Found your flights!")

    st.write("You could meet in one of the following destinations:")
    st.dataframe(best_flights_df)
