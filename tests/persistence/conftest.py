import esdbclient
import pytest


@pytest.fixture
def esdb_client() -> esdbclient.EventStoreDBClient:
    """Get an EventStoreDB client.

    :return: an instance of esdbclient.EventStoreDBClient
    """
    return esdbclient.EventStoreDBClient("esdb://localhost:2113?tls=false")
