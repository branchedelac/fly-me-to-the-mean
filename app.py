import datetime
import streamlit as st
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
import pandas as pd
import numpy as np

data_manager = DataManager()
flight_search = FlightSearch()
flight_data = FlightData()

with open("static/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

st.header("Helping you plan your international meetup since 2024.")
st.image("static/glass_onion_blanc_boarding.jpg")


with st.form("my_form"):
    with st.sidebar:
        st.write("From where, and when, would you and your friends like to travel?")

        travelling_from = st.text_input(
            label=":airplane: We are travelling from (e.g.: Paris, Berlin)"
        )
        from_date = st.date_input(":luggage: Earliest travel date")
        to_date = st.date_input(":luggage: Latest travel date")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")

if submitted:
    with st.spinner(
        f":sleuth_or_spy: Getting your best flights from: {travelling_from}..."
    ):
        st.write("Please enjoy some music while you wait!")
        st.audio(
            "static/Fly Me To The Moon _Remastered_.mp3",
            format="audio/mp3",
            start_time=0,
            sample_rate=None,
            end_time=None,
            loop=False,
        )
        departures_list = [
            {"city": city.strip()} for city in travelling_from.split(",")
        ]
        st.write("Searching for available flights...")
        departure_data = flight_search.get_city_id(departures_list)

        all_flights = flight_search.get_cheap_flights(
            departure_data, from_date, to_date
        )

        if not all_flights:
            st.write("No flights to shared destinations found for these dates.")

        else:
            st.write("Analyzing the results...")

            shared_destination_flights = flight_data.filter_by_shared_destinations(
                all_flights
            )

            # Work with the data
            if not shared_destination_flights:
                st.write("No flights to shared destinations found for these dates.")
            else:
                structured_shared_flights = flight_data.structure_flight_data(
                    shared_destination_flights
                )

                # Get top five € cheapest flight combinations
                (
                    destination_options,
                    individual_flights,
                    best_destination,
                    best_price,
                ) = flight_data.get_best_group_deal(structured_shared_flights)

                st.divider()
                st.header(f"Your ideal destination is... {best_destination}!")

                # Get a map!
                lats = []
                lons = []
                for d in departures_list:
                    lat, lon = flight_search.get_coordinates(d["city"])
                    lats.append(lat)
                    lons.append(lon)

                lat, lon = flight_search.get_coordinates(best_destination)
                lats.append(lat)
                lons.append(lon)
                print(lats)

                map = pd.DataFrame(
                    {
                        "lat": lats,
                        "lon": lons
                    }
                )
                st.map(map)

                st.write(
                    f"You can travel there for a total price of €{str(best_price)}, or €{str(round(best_price/len(departures_list), 2))} per person."
                )

                st.subheader("Ticket infotrmation")
                st.dataframe(individual_flights, hide_index=True)

                # Dispaly other possible destinations
                st.header(f"Here are the other options!")
                destination_options_columns = (
                    {
                        "city_to": "Destination",
                        "price": "Price",
                        "distance": "Distance",
                        "CO2 (mt)": "CO2 (mt)",
                        "CO2 (km)": "CO2 (km)",
                    },
                )
                st.dataframe(
                    destination_options,
                    column_config=destination_options_columns,
                    hide_index=True,
                )
