import pandas as pd


class FlightData:
    def __init__(self):
        pass

    def filter_by_shared_destinations(self, flight_data: dict):
        shared_destinations = set()
        best_flights = []
        # Identify destinations available for all origins
        for city, flights in flight_data.items():
            city_destinations = {
                f["cityTo"] for f in flights if f.get("availability", {}).get("seats")
            }
            # city_destinations.add(city)
            if shared_destinations:
                shared_destinations = shared_destinations.intersection(
                    city_destinations
                )
            else:
                shared_destinations = city_destinations
        print("Found the following shared destinations:", shared_destinations)
        # Loop through the flights again to get all flights heading for those destinations
        print("Getting available flights for shared destinations...")
        if len(shared_destinations) == 0:
            print("No shared destinations found.")
            return shared_destinations
        best_flights = []
        for flights in flight_data.values():
            city_flights = [
                f
                for f in flights
                if f.get("cityTo", "") in shared_destinations
                and f.get("availability", {}).get("seats")
            ]
            best_flights.extend(city_flights)
        print(
            "Flights with available seats reachable from all origins", len(best_flights)
        )
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

        flights_df = pd.DataFrame.from_records(structured_flight_data)

        return flights_df

    def get_best_group_deal(self, flights: pd.DataFrame) -> tuple:
        # Deduplicate the flights by combination of origin and destination city
        # Keep the cheapest flight for each combination
        print(flights)
        deduplicated_flights = (
            flights.sort_values(by="price", ascending=True)
            .groupby(["city_from", "city_to"])
            .agg("first")
        ).reset_index()

        deduplicated_flights.sort_values(by=["city_from", "city_to"])
        print(deduplicated_flights)

        # Sum the prices for each destination city
        group_prices = (
            deduplicated_flights.groupby(["city_to"])
            .agg({"price": "sum"})
            .sort_values("price")
            .reset_index()
        )
        best_destination = group_prices.iloc[0]
        print(best_destination)

        # Get the individual flights for the top destination
        group_best_flights = deduplicated_flights.loc[
            deduplicated_flights["city_to"] == best_destination["city_to"]
        ]
        print(group_best_flights)

        # Reorder the columns
        group_best_flights["From"] = (
            group_best_flights["city_from"]
            + " ("
            + group_best_flights["airport_from"]
            + ")"
        )
        group_best_flights["To"] = (
            group_best_flights["city_to"]
            + " ("
            + group_best_flights["airport_to"]
            + ")"
        )
        group_best_flights = group_best_flights.rename(
            columns={
                "departure": "Departure date",
                "distance": "Distance",
                "airlines": "Airline(s)",
                "price": "Ticket price",
            }
        )
        group_best_flights = group_best_flights[
            ["From", "To", "Departure date", "Ticket price", "Airline(s)", "Distance"]
        ]

        # Return
        return (
            group_best_flights,
            best_destination["city_to"],
            best_destination["price"],
        )
