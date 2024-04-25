import pandas as pd


class FlightData:
    def __init__(self):
        pass

    def filter_by_shared_destinations(self, flight_data: dict):
        shared_destinations = set()
        best_flights = []
        # Identify destinations available for all origins
        for city, flights in flight_data.items():
            city_destinations = {f["cityTo"] for f in flights}
            city_destinations.add(city)
            if shared_destinations:
                shared_destinations = shared_destinations.intersection(
                    city_destinations
                )
            else:
                shared_destinations = city_destinations
        print("Found the following shared destinations:", shared_destinations)
        # Loop through the flights again to get all flights heading for those destinations
        print("Getting flights for shared destinations...")
        best_flights = []
        for flights in flight_data.values():
            city_flights = [
                f
                for f in flights
                if (
                    f.get("cityTo", "") in shared_destinations
                    and f.get("availability", {}).get("seats")
                )
            ]
            best_flights.extend(city_flights)
        return best_flights

    def filter_available_and_cheapest(self, flight_data: dict):
        cheap_flights_list = []
        for city in flight_data:
            flights = [
                f for f in flight_data[city] if f.get("availability", {}).get("seats")
            ]
            cheap_flights_list.extend(flights[:1])
        return cheap_flights_list

    def structure_flight_data(self, fligth_data) -> pd.DataFrame:
        structured_flight_data = []
        for flight in fligth_data:
            flight_summary = {
                "airport_from": flight["flyFrom"],
                "airport_to": flight["flyTo"],
                "city_from": flight["cityFrom"],
                "city_to": flight["cityTo"],
                "distance": flight["distance"],
                "price": flight["price"],
                "nights": flight["nightsInDest"],
                "seats": flight["availability"]["seats"],
                "airlines": " & ".join(flight["airlines"]),
                "departure": flight["local_departure"][:10],
            }
            structured_flight_data.append(flight_summary)

        print(structured_flight_data)
        flights_df = pd.DataFrame.from_records(structured_flight_data)

        return flights_df
