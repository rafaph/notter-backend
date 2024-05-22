import httpx


class AuthHttpClient:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def signup(self, body: dict[str, object]) -> httpx.Response:
        return await self._client.post("/auth/signup", json=body)
