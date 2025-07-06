import httpx


class TokenAuth(httpx.Auth):

    def __init__(self, token: str) -> None:
        self.token = token

    async def async_auth_flow(self, request: httpx.Request):
        token = self.token
        request.headers["Authorization"] = f"Bearer {token}"
        yield request

    def sync_auth_flow(self, request):
        token = self.token
        request.headers["Authorization"] = f"Bearer {token}"
        yield request
