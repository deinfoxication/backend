"""Index tests."""
from flask import json
from flask.helpers import url_for


def test_index_response(test_client):
    """Test if the default blueprint is configured."""
    response = test_client.get(url_for("default.index"))
    assert response.status_code == 200, "Wrong status code {} with body {!r}".format(
        response.status_code, response.data
    )
    data = json.loads(response.data.decode())
    assert data == {"it": "works"}
