from bling_api.bling import BlingApi
from bling_api.exceptions import BlingApiError
from requests_policy.http import http


class GetInfoProduct(BlingApi):

    def get_products(self):

        link = "https://www.bling.com.br/Api/v3/produtos/lojas"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        response = http.get(link, headers=headers)
        response = response.json()

        return response


try:
    p = GetInfoProduct()
    p.get_products()
except BlingApiError as err:
    print(str(err))
