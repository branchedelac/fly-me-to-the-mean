import pandas as pd
from emission_data import EmissionData


class FlightData:
    def __init__(self):
        self.emissions = EmissionData()

    def filter_by_shared_destinations(self, flight_data: dict, city_host: bool):
        counter = 0
        shared_destinations = set()
        best_flights = []
        # Identify destinations available for all origins
        for city, flights in flight_data.items():
            city_destinations = {
                f["cityTo"] for f in flights if f.get("availability", {}).get("seats")
            }
            if city_host:
                city_destinations.add(city)
            if counter == 0:
                shared_destinations = city_destinations
            else:
                shared_destinations = shared_destinations.intersection(
                    city_destinations
                )
                
            counter += 1
            print(f"Destinations found for {city}: {city_destinations}")
            # If shared destinations is ever empty at the end of a loop, return
            print("Shared destinations:", shared_destinations)
            if len(shared_destinations) == 0:
                print("No shared destinations found.")
                return shared_destinations
            
        print("Found the following shared destinations:", shared_destinations)
        # Loop through the flights again to get all flights heading for those destinations
        print("Getting available flights for shared destinations...")
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
                "stopovers": len(flight["route"]) - 1,
                "seats": flight["availability"]["seats"],
                "airlines": " & ".join(flight["airlines"]),
                "departure": flight["local_departure"][:10],
                "arrival": flight["local_arrival"][:10],
                "link": flight["deep_link"],
                "From": f'{flight["cityFrom"]} ({flight["flyFrom"]})',
                "To": f'{flight["cityTo"]} ({flight["flyTo"]})',
            }
            structured_flight_data.append(flight_summary)

        flights_df = pd.DataFrame.from_records(structured_flight_data)

        return flights_df

    def get_best_group_deal(self, flights: pd.DataFrame) -> tuple:
        # Deduplicate the flights by combination of origin and destination city
        # Keep the cheapest flight for each combination
        deduped_flights = (
            flights.sort_values(by="price", ascending=True)
            .groupby(["city_from", "city_to"])
            .agg("first")
        ).reset_index()

        deduped_flights.sort_values(by=["city_from", "city_to"])

        # Summarize info for each destination
        destination_options = (
            deduped_flights.groupby("city_to")
            .agg(
                {
                    "airport_from": ", ".join,
                    "price": "sum",
                    "distance": "sum",
                    "airport_to": "first",
                }
            )
            .reset_index()
        )
        # Enrich with CO2 emission data from https://docs.carboninterface.com/#/?id=flight
        try:
            destination_options["Total CO2 (kg)"] = destination_options.apply(
                lambda x: self.emissions.get_flight_emissions(
                    x["airport_to"], x["airport_from"]
                ),
                axis=1,
            )
            # Drop any empty columns (probably CO2 because I exceeded the API limit)
            destination_options = destination_options.dropna(axis=1, how="all")
        except ValueError as ve:
            print("Error getting CO2 emissions estimate:", ve)
            
        # Get the cheapest destination
        cheapest_destination = destination_options.sort_values("price").iloc[0]

        # Get the individual flights for the cheapest destination
        individual_flights = deduped_flights.loc[
            deduped_flights["city_to"] == cheapest_destination["city_to"]
        ]
        print(individual_flights)

        # Return
        return (
            destination_options,
            individual_flights,
            cheapest_destination["city_to"],
            cheapest_destination["price"],
        )
