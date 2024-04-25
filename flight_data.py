class FlightData:
    def __init__(self):
        pass

    def filter_common_destinations(self, flight_data: dict):
        common_destinations = set()
        # Identify destinations available for all origins
        for city_id, flights in flight_data:
            city_destinations = {f["cityTo"] for f in flights}
            city_destinations.add(city_id)
            if common_destinations:
                common_destinations = common_destinations.intersection(
                    city_destinations
                )
            else:
                common_destinations = city_destinations
        print("Common destinations:", common_destinations)

        for city in flight_data:
            flights = [
                f
                for f in flight_data[city]
                if f.get("flyTo", "") in common_destinations
            ]
            common_destination_flights.extend(flights)
        return common_destination_flights

    def filter_available_and_cheapest(self, flight_data: dict):
        cheap_flights_list = []
        for city in flight_data:
            flights = [
                f for f in flight_data[city] if f.get("availability", {}).get("seats")
            ]
            cheap_flights_list.extend(flights[:1])
        return cheap_flights_list

    def structure_flight_data(self, fligth_data):
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
                "departure": flight["route"][0]["local_departure"][:10],
                "return": flight["route"][1]["local_departure"][:10],
            }
            structured_flight_data.append(flight_summary)
        return structured_flight_data
    
