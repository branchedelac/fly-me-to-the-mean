#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import sys
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
flight_data = FlightData()
notification_manager = NotificationManager()

use_sheety = False
use_file = False

if use_sheety:
    sheet_data = data_manager.get_sheet_data()

    # Get IATA codes and add to sheet
    if not all(row["iataCode"] for row in sheet_data):
        sheet_data = flight_search.get_iata_codes(sheet_data)
        for row in sheet_data:
            data_manager.update_sheet_row(row["id"], row)
if use_file:
    sheet_data = data_manager.use_data_from_file()

else:
    origins = data_manager.get_origins_from_user()
    origins = flight_search.get_iata_codes(origins)

# Get cheap flights
cheap_flights = {}
print(f"Getting flights and destination for origin cities: {[o['city'] for o in origins]}")
for origin in origins:
    print(f"Getting flights departing from {origin['city']}...")
    origin_flights = flight_search.get_cheap_flights(origin)
    if origin_flights:
        cheap_flights[origin["city"]] = origin_flights

# Format flight data
print("\nGettting the best flights...")
common_flights = flight_data.filter_common_destinations(cheap_flights)
filtered_flights = flight_data.filter_available_and_cheapest(common_flights)
structured_flight_data = flight_data.structure_flight_data(filtered_flights)

for flight in structured_flight_data:
    print(flight)
