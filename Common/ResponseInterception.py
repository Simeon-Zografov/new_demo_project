import json
from mitmproxy import http, ctx


def load(loader):
    ctx.options.add_option(
        "test_name", str, "", "Name of the test case to determine response modification"
    )


def response(flow: http.HTTPFlow) -> None:
    test_name = ctx.options.test_name
    # Target the specific request URL
    if 'https://thinking-tester-contact-list.herokuapp.com/contacts' in flow.request.url:
        # Decode the JSON body of the response
        body = flow.response.text
        json_data = json.loads(body)
        print("Original Response JSON:", json_data)

        # Check and modify the JSON data
        if test_name == "contact_page_test_2":
            json_data = []  # Set the contact list to be empty

        # Encode the modified JSON back to the response
        modified_body = json.dumps(json_data)
        print("Modified Response JSON:", modified_body)
        flow.response.text = modified_body  # Update the response with the modified JSON
