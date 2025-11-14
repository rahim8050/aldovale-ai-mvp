import requests

resp = requests.post(
    "http://localhost:8000/api/v1/auth/token/",
    json={"api_key": "79DY7aQz6dLMLQTvOAuDY6oGYIcdOpHvO1YPocao_3I"},
    timeout=10,
)
print(resp.status_code)
print(resp.json())
