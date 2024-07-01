import frappe
from frappe.model.document import Document

class APIEndpoint(Document):
    @staticmethod
    def get_list(args):
        # Fetch data from API Provider Endpoint Table
        endpoints = []
        providers = frappe.get_all('API Provider', filters={'enabled': 1}, fields=['name'])

        for provider in providers:
            provider_doc = frappe.get_doc('API Provider', provider.name)
            for endpoint in provider_doc.endpoints:
                endpoints.append({
                    'provider': provider.name,
                    'endpoint': endpoint.endpoint,
                })

        return endpoints

    @staticmethod
    def get_count(args):
        return len(APIEndpoint.get_list(args))

    @staticmethod
    def get_stats(args):
        # Implement if you need additional statistics
        return {}

    def load_from_db(self):
        data = next((item for item in APIEndpoint.get_list({}) if item['name'] == self.name), None)
        if not data:
            frappe.throw(f"Document {self.name} not found")

        self.update(data)

    def db_insert(self, *args, **kwargs):
        frappe.throw("Insert operation is not permitted for virtual doctype")

    def db_update(self, *args, **kwargs):
        frappe.throw("Update operation is not permitted for virtual doctype")

    def delete(self):
        frappe.throw("Delete operation is not permitted for virtual doctype")


def get_data(**kwargs):
    return APIEndpoint.get_list(kwargs)