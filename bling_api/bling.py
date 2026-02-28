import base64
import os
from typing import Any

import requests
from bling_api import settings
from bling_api.exceptions import BlingAuthenticationError, BlingRequestError
from bling_api.schemas.get_products import GetProductsParamsSchema
from bling_api.schemas.produto import ProdutoSchema
from bling_api.schemas.vinculo_produto_loja import ProdutoLojaSchema
from requests_policy.http import http


class BlingApi:
    BASE_URL = "https://www.bling.com.br/Api/v3"
    TOKEN_URL = f"{BASE_URL}/oauth/token"

    def __init__(self, client_id: str = "", client_secret: str = ""):

        if client_id and client_secret:
            self.client_id = client_id
            self.client_secret = client_secret
        else:
            self.client_id = settings.CLIENT_ID
            self.client_secret = settings.CLIENT_SECRET

        self.get_access_token()
        self.get_refresh_token()

        self.generate_base64_credential()

        self.update_access_token()

    @staticmethod
    def _read_token_file(filename: str) -> str:
        token_path = os.path.join(settings.PATH_SRC, f"tokens/{filename}")
        try:
            with open(token_path, "r") as token_file:
                return token_file.read().strip()
        except FileNotFoundError:
            return ""

    @staticmethod
    def _write_token_file(filename: str, value: str) -> None:
        token_path = os.path.join(settings.PATH_SRC, f"tokens/{filename}")
        with open(token_path, "w") as token_file:
            token_file.write(value)

    def _base_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def _oauth_headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "1.0",
            "Authorization": f"Basic {self.credential_base64}",
        }

    def _build_url(self, path: str) -> str:
        path = path.lstrip("/")
        return f"{self.BASE_URL}/{path}"

    @staticmethod
    def _safe_json_response(response: requests.Response | None) -> dict[str, Any]:
        if response is None:
            return {}
        try:
            return response.json()
        except ValueError:
            return {}

    def _request_json(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        request_method = getattr(http, method)
        try:
            response = request_method(
                self._build_url(path), headers=self._base_headers(), **kwargs
            )
            return response.json()
        except requests.exceptions.HTTPError as err:
            response_body = self._safe_json_response(err.response)
            raise BlingRequestError(
                message=f"Erro HTTP em {method.upper()} {path}",
                status_code=err.response.status_code if err.response else None,
                response_body=response_body,
            ) from err

    def generate_base64_credential(self):

        if self.client_id and self.client_secret:
            credential_str = f"{self.client_id}:{self.client_secret}"
            credential_bytes = credential_str.encode("utf-8")
            base64_bytes = base64.b64encode(credential_bytes)

            self.credential_base64 = base64_bytes.decode("utf-8")
        else:
            raise BlingAuthenticationError(
                "client_id ou client_secret incorreto ou não encontrado"
            )

    def get_access_token(self):
        self.access_token = self._read_token_file("access_token.txt")

    def get_refresh_token(self):
        self.refresh_token = self._read_token_file("refresh_token.txt")

    def set_access_token(self, access_token: str):
        self._write_token_file("access_token.txt", access_token)

        self.get_access_token()

    def set_refresh_token(self, refresh_token: str):
        self._write_token_file("refresh_token.txt", refresh_token)

        self.get_refresh_token()

    def update_access_token(self):

        if self.access_token and self.refresh_token:
            body_message = {
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
            }

            try:
                response = http.post(
                    self.TOKEN_URL, headers=self._oauth_headers(), data=body_message
                ).json()
                refresh_token = response["refresh_token"]
                access_token = response["access_token"]

                self.set_refresh_token(refresh_token)
                self.set_access_token(access_token)

                print("TOKEN ATUALIZADO COM SUCESSO")

            except requests.exceptions.HTTPError as err:
                error = self._safe_json_response(err.response)
                type_error = error.get("error", {}).get(
                    "description", "Erro desconhecido"
                )

                if type_error == "The client credentials are invalid":
                    raise BlingAuthenticationError(
                        "client_id ou client_secret inválido!"
                    ) from err

                if type_error in {"Invalid refresh token", "Refresh token has expired"}:
                    self.set_access_token("")
                    self.set_refresh_token("")
                    self.generate_access_token()
                    return

                raise BlingAuthenticationError(type_error) from err

        else:
            self.generate_access_token()

    def generate_access_token(self, authorization_code: str | None = None):

        print("Gerar novo access_token")
        code_authorization = (
            authorization_code
            or os.getenv("BLING_AUTHORIZATION_CODE")
            or getattr(settings, "AUTHORIZATION_CODE", "")
        )

        if not code_authorization:
            code_authorization = input(
                "Cole aqui o code_authorization gerado no app do bling: "
            ).strip()

        if not code_authorization:
            raise BlingAuthenticationError("authorization_code não informado")

        body_message = {"grant_type": "authorization_code", "code": code_authorization}

        try:
            response = http.post(
                self.TOKEN_URL, headers=self._oauth_headers(), data=body_message
            ).json()
            refresh_token = response["refresh_token"]
            access_token = response["access_token"]

            self.set_refresh_token(refresh_token)
            self.set_access_token(access_token)

            print("TOKEN GERADO COM SUCESSO")

        except requests.exceptions.HTTPError as err:
            error = (
                self._safe_json_response(err.response)
                .get("error", {})
                .get("description", "Erro desconhecido")
            )
            match error:
                case "The authorization code has expired":
                    msg = "Código de autorização expirado, gere um novo e lembre-se que ele tem apenas 1 minuto de duração!"
                case "Authorization code doesn't exist or is invalid for the client":
                    msg = "Código de autorização inválido"
                case _:
                    msg = error
            raise BlingAuthenticationError(msg) from err

    def get_id_deposito(self):
        response = self._request_json("get", "depositos")

        print(response)

    def get_product(self, id_product):
        return self._request_json("get", f"produtos/{id_product}")

    def get_products(self, params: GetProductsParamsSchema | None = None):
        parsed_params = (
            params.model_dump(exclude_none=True)
            if hasattr(params, "model_dump")
            else params
        )
        return self._request_json("get", "produtos", params=parsed_params)

    def get_products_fornecedor(self, params: dict | None = None):
        return self._request_json("get", "produtos/fornecedores", params=params)

    def edit_product_fornecedor(self, produto_fornecedor_id: str, payload: dict):
        return self._request_json(
            "put", f"produtos/fornecedores/{produto_fornecedor_id}", json=payload
        )

    def create_product_fornecedor(self, payload: dict):
        return self._request_json("post", "produtos/fornecedores", json=payload)

    def get_product_variacoes(self, produto_pai_id: str):
        return self._request_json("get", f"produtos/variacoes/{produto_pai_id}")

    def edit_product(self, produto_pai_id: str, payload: dict):
        return self._request_json("patch", f"produtos/{produto_pai_id}", data=payload)

    def delete_products(self, params: list):
        return self._request_json("delete", "produtos", params=params, timeout=(10, 60))

    def get_nfs(self, situacao=1):
        return self._request_json("get", "nfe", params={"situacao": situacao})

    def get_contacts(self, pagina=1, limite=100):
        return self._request_json(
            "get", "contatos", params={"pagina": pagina, "limite": limite}
        )

    def create_product(self, product: ProdutoSchema):
        product_json = product.model_dump_json()

        response = self._request_json("post", "produtos", data=product_json)

        data = {
            "id_pai": response["data"]["id"],
            "variations": [
                {"id": var["id"], "nome": var["nomeVariacao"]}
                for var in response["data"]["variations"]["saved"]
            ],
        }
        return data

    def create_link_with_store(self, vinculo: ProdutoLojaSchema):
        payload = vinculo.model_dump_json()
        return self._request_json("post", "produtos/lojas", data=payload)
