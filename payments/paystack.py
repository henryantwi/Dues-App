import requests
from django.conf import settings


class Paystack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = "https://api.paystack.co"

    def verify_payment(self, ref, *args, **kwargs):
        path = f"/transaction/verify/{ref}"

        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        url = self.base_url + path

        try:
            response = requests.get(url, headers=headers)

            # Check the HTTP response status
            if response.status_code == 200:
                response_data = response.json()
                return (
                    response_data.get("status"),
                    response_data.get("data"),
                    response_data["data"].get("id"),
                )
            else:
                response_data = response.json()
                return response_data.get("status"), response_data.get("message")

        except requests.RequestException as e:
            print(f"Request Exception: {e}")
            return False, "Request Exception occurred"

        except Exception as e:
            print(f"Error verifying payment: {e}")
            return False, "Error verifying payment"

    def json_response(self):
        return self.response_data
