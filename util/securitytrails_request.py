import requests
import urllib.parse

class SecurityTrailsRequest:

    KEY = ""

    BASE_URL = "https://api.securitytrails.com/v1"

    headers = {
        'APIKEY': KEY
    }

    def get_neighbors(self, ip_address: str) -> dict:
        url = f"{self.BASE_URL}/ips/nearby/{ip_address}"

        result = requests.get(url, headers = self.headers)

        return result
