from httpx import AsyncClient
from pytest import fixture, mark


class TestHealthCheck:
    @fixture(autouse=True)
    def setup(self):
        self.url = '/'

    @mark.asyncio
    async def test_health_check_ok(self, client):
        assert isinstance(client, AsyncClient)
        response = await client.get(self.url)
        assert response.status_code == 200
        assert response.json() == {'message': 'OK'}
