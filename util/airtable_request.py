import requests
import urllib.parse

class AirtableRequest:

    KEY = ""

    BASE_URL = "https://api.airtable.com/v0"

    BASE_ID = "appTJAR7zX7X8Rrk6"

    headers = {
        'Authorization': f'Bearer {KEY}'
    }

    def get_total(self, table_id: str, view_id: str = None, fields: list = []) -> dict:
        compiled_fields = ""

        for field in fields:
            field = field.replace(" ", "+")

            compiled_fields += urllib.parse.quote(f"fields[]={field}&", safe = '&=+')

        compiled_fields = compiled_fields.rstrip("&")

        url = f"{self.BASE_URL}/{self.BASE_ID}/{table_id}"

        if view_id:
            url += f"/{view_id}"

        if compiled_fields:
            url += f"?{compiled_fields}"

        result = requests.get(url, headers = self.headers)

        return result

    def get_record(self, table_id, record_id):
        url = f"{self.BASE_URL}/{self.BASE_ID}/{table_id}/{record_id}"

        result = requests.get(url, headers = self.headers)

        return result

    def get_activity(self, table_id, view_id):
        sorting = urllib.parse.quote("sort[0][field]=Day&sort[0][direction]=desc", safe = '&=')

        url = f"{self.BASE_URL}/{self.BASE_ID}/{table_id}?view={view_id}&{sorting}"

        result = requests.get(url, headers = self.headers)

        return result
