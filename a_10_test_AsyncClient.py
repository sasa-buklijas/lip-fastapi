import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient

@pytest.mark.asyncio
async def test_all():
    from a_10_code import app

    # Manually trigger the lifespan context
    with TestClient(app) as _client_sync:
        pass  # This ensures that the lifespan runs and initializes the state

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
    #async with AsyncClient(app=app, base_url="http://localhost") as client:
        # Give time for the lifespan to initialize the state
        #await asyncio.sleep(1)

        r = await client.get("/state/")
        assert r.status_code == 200
        #print(f'{r.json()=}')
        assert r.json() == {'rw': 1}
