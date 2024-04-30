import os
import requests
from dotenv import load_dotenv
import datetime as dt
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

    def get_flight_emissions(self, destination: str, departures: str) -> dict:
        endpoint = f"{self.base_url}/estimates"
        print(f"Getting emission estimate for {departures} -> {destination}")
        legs = []
        for departure in departures.split(","):
            legs.append(
                    {
                        "departure_airport": departure.strip(),
                        "destination_airport": destination,
                    }            )

        body = {"type": "flight", "passengers": 1, "legs": legs}
        request = requests.post(endpoint, json=body, headers=self.headers)
        print(request.status_code)
        if request.status_code >= 400:
            print(request.text)
        else:
            data = request.json()["data"]["attributes"]
            return pd.Series([data["carbon_mt"],data["carbon_kg"]])
