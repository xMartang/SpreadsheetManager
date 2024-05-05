def test_root_redirect_to_docs(http_client):
    response = http_client.get("/")

    assert response.status_code == 200
    assert str(response.url).endswith('/docs')
