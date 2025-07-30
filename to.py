import base64
import requests

client_id = "435c1b9c9abc4673b1f119d6ca91f54b"
client_secret = "31682233f90b4c7dbd7ecd0daf5179f6"

auth_str = f"{client_id}:{client_secret}"
b64_auth_str = base64.b64encode(auth_str.encode()).decode()

headers = {
    "Authorization": f"Basic {b64_auth_str}",
    "Content-Type": "application/x-www-form-urlencoded"
}

data = {
    "grant_type": "client_credentials"
}

response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)

if response.status_code == 200:
    access_token = response.json().get("access_token")
    print("Your token:", access_token)
else:
    print("Request failed.")
    print("Status code:", response.status_code)
    print("Response:", response.text)
