from bs4 import BeautifulSoup 
import requests

url = "http://127.0.0.1:8000/protected"
headers = {"Authorization": "Bearer your_token"}
response = requests.get(url, headers=headers)

print(response.json())  # Check response
