import requests
import frappe
from frappe.model.document import Document
import csv
from datetime import datetime
import os

class CryptoData(Document):
    """This is a virtual doctype controller for the CryptoData doctype.
    
    - It fetches data from the CoinGecko API as the "backend".
    - Key is the docname and value is the document itself.
    """



    @staticmethod
    def fetch_data() -> dict[str, dict]:
        """Read data from CSV and return as dictionary"""
        date_str = datetime.now().strftime('%Y-%m-%d')
        file_path = f'./csv_data/collection-{date_str}.csv'
        if not os.path.exists(file_path):
            frappe.throw("Data not found for today. Please collect data first.")

        data_dict = {}
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data_dict[row['id']] = row

        return data_dict

    def db_insert(self, *args, **kwargs):
        # Insert should not be used in this read-only virtual doctype
        frappe.throw("Insert operation is not permitted for virtual doctype using API data")

    def db_update(self, *args, **kwargs):
        # Update should not be used in this read-only virtual doctype
        frappe.throw("Update operation is not permitted for virtual doctype using API data")

    def delete(self):
        # Delete should not be used in this read-only virtual doctype
        frappe.throw("Delete operation is not permitted for virtual doctype using API data")

    def load_from_db(self):
        data = self.fetch_data()
        d = data.get(self.name)
        if not d:
            frappe.throw(f"Document {self.name} not found")
        super(Document, self).__init__(d)

    @staticmethod
    def get_list(args):
        data = CryptoData.fetch_data()
        return [frappe._dict(doc) for name, doc in data.items()]

    @staticmethod
    def get_count(args):
        data = CryptoData.fetch_data()
        return len(data)

    @staticmethod
    def get_stats(args):
        # Additional statistics can be added here if needed
        return {}

@frappe.whitelist()
def get_crypto_data():
    return CryptoData.get_list({})
