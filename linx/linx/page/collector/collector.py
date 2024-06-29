import frappe
import csv
import requests
import os
from datetime import datetime

class Collector:
    """This is a virtual doctype controller for the Collector doctype.
    
    - It fetches data from various CoinGecko API Endpoint.
    - Key is the docname and value is the document itself.
    """

    API_URLS = {
        "simple": "https://api.coingecko.com/api/v3/simple",
        "coins": "https://api.coingecko.com/api/v3/coins/markets",
        "contract": "https://api.coingecko.com/api/v3/coins/{id}/contract",
        "asset_platforms": "https://api.coingecko.com/api/v3/asset_platforms",
        "coins/categories": "https://api.coingecko.com/api/v3/coins/categories",
        "nfts": "https://api.coingecko.com/api/v3/nfts",
        "onchain": "https://api.coingecko.com/api/v3/onchain",
        "exchanges": "https://api.coingecko.com/api/v3/exchanges",
        "derivatives": "https://api.coingecko.com/api/v3/derivatives",
        "search": "https://api.coingecko.com/api/v3/search",
        "search/trending": "https://api.coingecko.com/api/v3/search/trending",
        "global": "https://api.coingecko.com/api/v3/global",
        "companies": "https://api.coingecko.com/api/v3/companies"
    }

    PARAMS = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": False
    }

    @staticmethod
    def collect_data(endpoint: str) -> str:
        """Fetch data from the selected CoinGecko API endpoint and save to CSV"""
        if endpoint not in Collector.API_URLS:
            frappe.throw("Invalid endpoint selected")

        url = Collector.API_URLS[endpoint]
        if '{id}' in url:
            # Placeholder for dynamic id handling
            url = url.replace('{id}', 'bitcoin')  # Example using 'bitcoin', adjust as needed

        response = requests.get(url, params=Collector.PARAMS)
        if response.status_code != 200:
            frappe.throw(f"Failed to fetch data from CoinGecko API. Status code: {response.status_code}")

        data = response.json()

        # Save data to CSV
        if not os.path.exists('./csv_data'):
            os.makedirs('./csv_data')

        file_path = f'./csv_data/{endpoint}.csv'
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = data[0].keys() if isinstance(data, list) and data else data.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            if isinstance(data, list):
                for item in data:
                    writer.writerow(item)
            else:
                writer.writerow(data)

        # Update endpoint status after successful collection
        Collector.update_endpoint_status(endpoint, file_loaded=True, last_collection_date=datetime.now())

        return "Data collected and saved successfully."

    @staticmethod
    def fetch_data(endpoint: str) -> dict:
        """Read data from CSV and return as dictionary"""
        file_path = f'./csv_data/{endpoint}.csv'
        if not os.path.exists(file_path):
            frappe.throw("Data not found for today. Please collect data first.")

        data_dict = {}
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data_dict[row['id']] = row

        return data_dict

    @staticmethod
    def update_endpoint_status(endpoint: str, file_loaded=False, last_collection_date=None):
        """Update endpoint status in Frappe database"""
        doc = frappe.get_doc('API Endpoint', {
            'endpoint': endpoint
        })
        doc.file_loaded = file_loaded
        doc.last_collection_date = last_collection_date
        doc.save(ignore_permissions=True)

    @staticmethod
    def get_endpoint_status():
        """Retrieve endpoint statuses from Frappe database"""
        Endpoint = frappe.get_all('API Endpoint')

        return Endpoint

@frappe.whitelist()
def collect_data(endpoint: str) -> str:
    """Wrapper function for collect_data method"""
    return Collector.collect_data(endpoint)

@frappe.whitelist()
def fetch_data(endpoint: str) -> dict:
    """Wrapper function for fetch_data method"""
    return Collector.fetch_data(endpoint)

@frappe.whitelist()
def get_endpoint_status() -> list:
    """Wrapper function for get_endpoint_status method"""
    return Collector.get_endpoint_status()
