import csv
import json
import os
import requests
from dotenv import load_dotenv
import sys


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        load_dotenv()
        self.sheety_user = os.environ.get("SHEETY_USER")
        self.sheety_token = os.environ.get("SHEETY_TOKEN")
        self.headers = {
            "Authorization": self.sheety_token,
            "Content-Type": "application/json",
        }

    def get_sheet_data(self):
        endpoint = f"https://api.sheety.co/{self.sheety_user}/flightDeals/prices"
        response = requests.get(url=endpoint, headers=self.headers)
        response.raise_for_status()
        sheet_data = response.json()["prices"]
        return sheet_data

    def update_sheet_row(self, row_id: int, updated_data: dict):
        endpoint = (
            f"https://api.sheety.co/{self.sheety_user}/flightDeals/prices/{row_id}"
        )
        data_to_put = {"price": updated_data}
        response = requests.put(url=endpoint, json=data_to_put, headers=self.headers)
        response.raise_for_status()

    def use_data_from_file(self):
        with open("destinations.csv") as f:
            data = csv.DictReader(f)
            return list(data)

    def get_origins_from_user(self):
        return [{"city": arg} for arg in sys.argv[1:]]
