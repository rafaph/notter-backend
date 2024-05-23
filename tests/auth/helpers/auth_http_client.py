import httpx


class AuthHttpClient:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def signup(self, body: dict[str, object]) -> httpx.Response:
        return await self._client.post("/auth/signup", json=body)

    async def token(self, body: dict[str, object]) -> httpx.Response:
        return await self._client.post("/auth/token", data=body)

    async def profile(self, token: str | None = None) -> httpx.Response:
        headers = {"Authorization": f"Bearer {token}"} if token else None
        return await self._client.get("/auth/profile", headers=headers)
