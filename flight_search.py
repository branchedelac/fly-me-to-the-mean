import os
import requests
from dotenv import load_dotenv
import datetime as dt


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def __init__(self):
        load_dotenv()
        self.kiwi_user = os.environ.get("KIWI_USER")
        self.kiwi_key = os.environ.get("KIWI_KEY")
        self.base_url = "https://api.tequila.kiwi.com"
        self.headers = {"Content-Type": "application/json", "apikey": self.kiwi_key}
        self.today = dt.datetime.today()
        self.months_from_today = self.today + dt.timedelta(days=30)

    def get_city_id(self, cities) -> dict:
        endpoint = f"{self.base_url}/locations"
        for city in cities:
            query = f"/query?term={city['city']}&location_types=city"
            response = requests.get(url=endpoint + query, headers=self.headers)
            response.raise_for_status()
            city_data = response.json()
            if city_data["results_retrieved"] > 0:
                city["city_id"] = city_data["locations"][0]["id"]
        return cities

    def get_coordinates(self, city) -> tuple:
        endpoint = f"{self.base_url}/locations"
        query = f"/query?term={city}&location_types=city"
        response = requests.get(url=endpoint + query, headers=self.headers)
        print(query)
        response.raise_for_status()
        city_data = response.json()
        if city_data["results_retrieved"] > 0:
            return (
                city_data["locations"][0]["location"]["lat"],
                city_data["locations"][0]["location"]["lon"],
            )

    def get_shared_destinations(self, departure_cities) -> set:
        params = {
            "term": "",
            "limit": 500,
            "sort": "name",
            "active_only": True,
            "source_popularity": "bookings",
        }
        for i, city in enumerate(departure_cities):
            params["term"] = city["city_id"]
            response = requests.get(
                f"{self.base_url}/locations/topdestinations",
                params=params,
                headers=self.headers,
            )
            response.raise_for_status()
            if response.status_code == 200:
                data = response.json()
                print(f"{data['results_retrieved']} results retrieved for {city}")
                retrieved_locations = {
                    (location["id"], location["name"]) for location in data["locations"]
                }
                retrieved_locations.add((city["city_id"], city["city"]))
                if i == 0:
                    all_results = retrieved_locations
                else:
                    all_results = all_results.intersection(retrieved_locations)
            else:
                print(
                    f"Something went wrong for {city['city_id']}! Status: {response.status_code}"
                )
        return all_results

    def get_cheap_flights(self, departure_cities, date_from, date_to):
        all_flights = {}
        endpoint = f"{self.base_url}/v2/search?query="
        params = {
            "date_from": date_from.strftime("%d/%m/%Y"),
            "date_to": date_to.strftime("%d/%m/%Y"),
            "price_to": 2000,
            "nights_in_dst_from": 1,
            "nights_in_dst_to": 30,
            "one_for_city": True,
            "one_per_date": True,
            "curr": "EUR",
            "max_stopovers": 0,
            "limit": 500,
        }
        for i, city in enumerate(departure_cities):
            params["fly_from"] = city["city_id"]

            # Make request
            result = requests.get(endpoint, params=params, headers=self.headers)
            result.raise_for_status()
            json = result.json()
            print(f"{json['_results']} results retrieved for {city['city']}")
            all_flights[city["city"]] = json["data"]

            if not json["data"]:
                return {}

        return all_flights
