import frappe
from frappe.model.document import Document


class APIEndpoint(Document):

    @staticmethod
    def get_list(args):
        return frappe.get_all("API Provider Endpoint Table", fields=["name", "url"])

    @staticmethod
    def get_count(args):
        return len(APIEndpoint.get_list(args))

    @staticmethod
    def get_stats(args):
        # Implement if you need additional statistics
        return {}

    def load_from_db(self):
        data = next(
            (item for item in APIEndpoint.get_list({}) if item["name"] == self.name),
            None,
        )
        if not data:
            frappe.throw(f"Document {self.name} not found")

        self.update(data)
        pass

    def db_insert(self, *args, **kwargs):
        pass

    def db_update(self, *args, **kwargs):
        # frappe.throw("Update operation is not permitted for virtual doctype")
        pass

    def delete(self):
        # frappe.throw("Delete operation is not permitted for virtual doctype")
        pass


@frappe.whitelist()
def get_data(**kwargs):
    return APIEndpoint.get_list(kwargs)
