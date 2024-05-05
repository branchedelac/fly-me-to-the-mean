import os
import requests
from dotenv import load_dotenv
import pandas as pd


class EmissionData:
    # This class is responsible for talking to the Flight Search API.

    def __init__(self):
        load_dotenv()
        self.ci_key = os.environ.get("CARBON_INTERFACE_KEY")
        self.base_url = "https://www.carboninterface.com/api/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.ci_key}",
        }

    def get_flight_emissions(self, destination: str, departures: str) -> pd.Series:
        try:
            endpoint = f"{self.base_url}/estimates"
            print(f"Getting emission estimate for {departures} -> {destination}")
            legs = []
            for departure in departures.split(","):
                legs.append(
                    {
                        "departure_airport": departure.strip(),
                        "destination_airport": destination,
                    }
                )

            body = {"type": "flight", "passengers": 1, "legs": legs}

            result = requests.post(endpoint, json=body, headers=self.headers)
            result.raise_for_status()

            data = result.json()["data"]["attributes"]
            return pd.Series([data["carbon_kg"]])

        except requests.exceptions.HTTPError as he:
            print(he)
