from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_default_temperature_endpoint():
    response = client.get("/temperature")
    assert response.status_code == 200
    assert "message" in response.json()

def test_specific_city_temperature_endpoint():
    response = client.get("/temperature?city=Porto")
    assert response.status_code == 200
    assert "Porto" in response.json()["message"]

def test_temperature_endpoint_with_unit():
    response = client.get("/temperature?city=Lisbon&unit=F")
    assert response.status_code == 200
    assert "°F" in response.json()["message"]

def test_default_rain_endpoint():
    response = client.get("/rain")
    assert response.status_code == 200
    assert "message" in response.json()

def test_specific_city_rain_endpoint():
    response = client.get("/rain?city=Porto")
    assert response.status_code == 200
    assert "Porto" in response.json()["message"]

def test_invalid_city_temperature_endpoint():
    response = client.get("/temperature?city=InvalidCity123")
    assert response.status_code == 404

def test_invalid_city_rain_endpoint():
    response = client.get("/rain?city=InvalidCity123")
    assert response.status_code == 404

def test_invalid_endpoint():
    response = client.get("/invalid_endpoint")
    assert response.status_code == 404

def test_temperature_for_unsupported_days():
    response = client.get("/temperature?city=Lisbon&days=11")  # Assuming 10 is the max supported
    assert response.status_code == 400
    assert "must be between" in response.json()["detail"]

def test_rain_for_unsupported_days():
    response = client.get("/rain?city=Lisbon&days=11")  # Assuming 10 is the max supported
    assert response.status_code == 400
    assert "must be between" in response.json()["detail"]

def test_invalid_unit_parameter():
    response = client.get("/temperature?city=Lisbon&unit=X")  # Testing Invalid unit
    assert response.status_code == 400
    assert "Invalid unit parameter" in response.json()["detail"]

def test_temperature_for_specific_day():
    response = client.get("/temperature?city=Lisbon&days=3")
    assert response.status_code == 200
    assert "in 3 days" in response.json()["message"]

def test_rain_for_specific_day():
    response = client.get("/rain?city=Lisbon&days=3")
    assert response.status_code == 200
    assert "in 3 days" in response.json()["message"]
