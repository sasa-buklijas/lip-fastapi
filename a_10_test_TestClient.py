from fastapi.testclient import TestClient

def test_all():
    from a_10_code import app 

    # Manually trigger the lifespan context
    with TestClient(app) as _client_sync:
        pass  # This ensures that the lifespan runs and initializes the state
    # found this by molesting ChatGTP :-)
    # but this will start it and stop it

    # so here lifespan is still not running
    client = TestClient(app)

    response = client.get("/state/")
    assert response.status_code == 200
    assert response.json() == {'rw': 1}
