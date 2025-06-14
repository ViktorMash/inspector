import requests
import sys

from app.core import settings
from app.power_bi.authentication import auth
from app.schemas import (
    AuthErrorSchema,
    ResponseSchema, ResponseErrorSchema
)


class MakeRequest:
    def __init__(self, params, auth_token):
        self.base_url = params.POWER_BI_BASE_URL
        self.token = auth_token.generate_token()

    def request_get(self, request_str: str):
        """ make get request to power bi API """

        if isinstance(self.token, AuthErrorSchema):
            print(f"Authentication failed: {self.token}")
            sys.exit(1)

        response = requests.get(
            url=f"{self.base_url}/{request_str}",
            headers={'Authorization': f'{self.token.access_token}'},
        )

        if response.status_code != 200:
            error_data = ResponseErrorSchema.model_validate(response)
            return error_data.model_dump(by_alias=True)

        print(request_str, response.json())
        validated_response = ResponseSchema.model_validate(response)
        return validated_response.model_dump(by_alias=True)

request = MakeRequest(settings, auth)