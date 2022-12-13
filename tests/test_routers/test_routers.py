import json
import pytest
from dataclasses import asdict
from fastapi.testclient import TestClient
from app.main import app


# CONSTANTS
def get_client():
    """
    Get the fastapi test client.
    :return:
    """
    return TestClient(app)


def get_some_other_static_info():
    """
    Use functions outside of the TestClass-Scope to get global infos
    :return:
    """
    return "ThisIsAnGlobalInfo"

class TestConfigRouter:
    """
    Tests for the config router
    """

    def test_health_endpoint(self):
        # get the test client (Test instance of the fastapi-app)
        client = get_client()
        # the enpoint to test
        endpoint = "/actuator/health/"
        # Make the appropriate request
        response = client.get(endpoint)
        # do the needed testing with assert
        assert response.status_code == 200
        # just optinal printing for you
        print(response.json())
