# import pytest_asyncio
# import httpx
# from typing import AsyncGenerator

# @pytest_asyncio.fixture()
# async def get_client() -> AsyncGenerator[httpx.AsyncClient]:
#     from a_10_code import app
#     transport = httpx.ASGITransport(app=app)

#     async with httpx.AsyncClient(
#         transport=transport,
#         base_url="http://testserver"
#     ) as client:
#         yield client

# async def test_all(get_client: httpx.AsyncClient):
#     response = await get_client.get("/state")
#     assert response.status_code == 200
#     assert response.json() == {'rw': 0}



import pytest_asyncio
import pytest
import asyncio

from fastapi.testclient import TestClient
from a_10_code import app

@pytest_asyncio.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

@pytest.mark.asyncio
async def test_state(client):
    response = client.get("/state/")
    assert response.status_code == 200
    assert response.json() == {"rw": 1}

    await asyncio.sleep(11)

    response = client.get("/state/")
    assert response.status_code == 200
    assert response.json() == {'rw': 2}