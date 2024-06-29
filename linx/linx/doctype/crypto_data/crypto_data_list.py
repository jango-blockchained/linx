# in your_app/your_app/doctype/crypto_data/crypto_data_list.py
from frappe import _

def get_context(context):
    context.no_cache = 1

    # Fetch data using the CryptoData class
    from .crypto_data import CryptoData
    context.data = CryptoData.get_data()