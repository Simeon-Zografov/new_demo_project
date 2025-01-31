import requests


def get_bearer_token():
    # Point 1
    # Set the URL
    url = "https://thinking-tester-contact-list.herokuapp.com/users/login"
    # Set the body
    body = {
        "email": "simeon.hhl.qa@gmail.com",
        "password": "Test#1234"
    }
    # Point 2
    # Send the request and save the response in the response variable
    response = requests.post(url, json=body)
    # Point 3
    # Check what is response status code
    if response.status_code == 200:
        # Point 4
        # Extract the bearer token and return it
        response_data = response.json()
        bearer_token = response_data.get("token")
        return bearer_token
    else:
        # Print messages in case the status code is different
        print("Request failed with status code:", response.status_code)
        print("Response content:", response.text)


def get_contact_list():
    # Point 1
    # Set the URL
    url = "https://thinking-tester-contact-list.herokuapp.com/contacts"
    # Get the token with the 'get_bearer_token' method
    token = get_bearer_token()
    # Set the headers
    headers = {
        "Authorization": f"Bearer {token}"
    }
    # Point 2
    # Send the request and save the response in the response variable
    response = requests.get(url, headers=headers)
    # Point 3
    # Check what is response status code
    if response.status_code == 200:
        response_data = response.json()
        names = {}
        # Point 4
        # Iterate through all contacts in the response and save the names in the 'names' dictionary
        for contact in response_data:
            contact_id = contact["_id"]
            first_name = contact["firstName"]
            last_name = contact["lastName"]
            names[contact_id] = {"first_name": first_name, "last_name": last_name}
        # Point 5
        # Return the dictionary
        return names
    else:
        # Print messages in case the status code is different
        print("Request failed with status code:", response.status_code)
        print("Response content:", response.text)
