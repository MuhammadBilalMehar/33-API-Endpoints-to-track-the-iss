import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

response = requests.get(url)

print(response.status_code)   # 200 means success
print(response.json())        # API data



# post api requests 

import requests

url = "https://jsonplaceholder.typicode.com/posts"

data = {
    "title": "API Integration",
    "body": "Learning API with Python",
    "userId": 1
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())


#headers for authentication

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY"
}

response = requests.get(url, headers=headers)



#authentication types

# api key 
params = {"api_key": "YOUR_KEY"}
requests.get(url, params=params)

# bearer token
headers = {"Authorization": "Bearer token_here"}

#basic authentication
requests.get(url, auth=("username", "password"))




# handeling json response 
if response.status_code == 200:
    data = response.json()
    print(data["title"])
else:
    print("API Error")

# error handeling 
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.HTTPError:
    print("HTTP error")
except Exception as e:
    print("Error:", e)



