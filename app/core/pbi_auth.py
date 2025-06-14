import msal

from app.core import settings
from app.schemas import TokenSchema, AuthErrorSchema


class PowerBIAuth:
    def __init__(self, params):
        self.app_id=params.APP_ID
        self.auth_url=params.AUTH_URL
        self.secret_value=params.SECRET_VALUE
        self.user_email=params.USER_EMAIL
        self.user_password=params.USER_PASSWORD
        self.scopes=params.SCOPES
        self.token_type=params.TOKEN_TYPE

        self.token_strategies = {
            "app": self._app_token,
            "user": self._user_token
        }

    def _app_token(self):
        client = msal.ConfidentialClientApplication(
            self.app_id,
            authority=self.auth_url,
            client_credential=self.secret_value
        )
        return client.acquire_token_for_client(scopes=self.scopes)

    def _user_token(self):
        client = msal.PublicClientApplication(
            self.app_id,
            authority=self.auth_url
        )
        return client.acquire_token_by_username_password(
            username=self.user_email,
            password=self.user_password,
            scopes=self.scopes
        )

    def generate_token(self) -> TokenSchema | AuthErrorSchema:
        """ get token for application (service principal) to access power bi api """

        if self.token_type not in self.token_strategies:
            raise ValueError(f"Unknown token type: {self.token_type}")

        response = self.token_strategies[self.token_type]()

        if "access_token" not in response:
            response_with_source = {**response, "source": f"{self.token_type} token"}
            return AuthErrorSchema.model_validate(response_with_source)

        return TokenSchema.model_validate(response)


auth = PowerBIAuth(settings)