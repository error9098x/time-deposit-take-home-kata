import os
import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import text
from fastapi.testclient import TestClient

# Skip this file if Docker is not available/running (e.g., CI without Docker Desktop)
DOCKER_AVAILABLE = True
if os.getenv("SKIP_INTEGRATION") == "1":
    DOCKER_AVAILABLE = False
else:
    try:
        import docker  # provided transitively by testcontainers
        docker.from_env().ping()
    except Exception:
        DOCKER_AVAILABLE = False

pytestmark = pytest.mark.skipif(not DOCKER_AVAILABLE, reason="Docker daemon not available; set SKIP_INTEGRATION=1 to skip explicitly")

from app.main import app
from app.infrastructure.database import engine, Base


@pytest.fixture(scope="session")
def postgres_container():
    # Use PostgresContainer without deprecated wait decorators
    container = PostgresContainer("postgres:16-alpine")
    with container as postgres:
        os.environ["DATABASE_URL"] = postgres.get_connection_url()
        yield postgres


@pytest.fixture(scope="session", autouse=True)
def setup_db(postgres_container):
    # Recreate tables against the Postgres engine
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_api_endpoints_with_postgres(postgres_container):
    client = TestClient(app)

    # Initially should be empty
    r = client.get("/time-deposits")
    assert r.status_code == 200
    assert r.json() == []

    # Seed three rows directly via SQL to avoid coupling to seed.py
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO time_deposits (planType, days, balance) VALUES
            ('basic', 45, 1234.56),
            ('student', 200, 2000.00),
            ('premium', 50, 5000.00);
        """))

    r = client.get("/time-deposits")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 3

    # Update balances
    r = client.post("/time-deposits/update-balances")
    assert r.status_code == 200
    updated = r.json()
    assert len(updated) == 3

    # Spot check one calculation (basic plan after 30 days)
    basic = next(x for x in updated if x["planType"] == "basic")
    # 1% annual -> per month 0.8333.. -> 0.83; 1234.56 + 0.83 = 1235.39
    assert float(basic["balance"]) == pytest.approx(1235.39, rel=1e-3, abs=1e-2)

