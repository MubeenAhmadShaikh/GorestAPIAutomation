import time
import requests
from jsonschema import validate, exceptions
import random
from utilities.base import Base
# validate status codes
def validate_status_code(response, expected_code):
    handle_too_many_request_429(response)
    assert response.status_code == expected_code, f"Expected {expected_code} Got unexpected status code: " \
                                              + str(response.status_code)
# validate_auth_token()
def validate_auth_token(response, token):
    authorization_token = response.request.headers.get("Authorization")
    assert authorization_token == "Bearer " + token, "Unexpected Auth token: " + authorization_token


# validate_content_type()
def validate_content_type(response):
    content_type = response.headers.get("Content-Type")
    assert content_type == "application/json; charset=utf-8", "Unexpected Content-Type: " + str(content_type)


# validate content type is none
def validate_none_content_type(response):
    content_type = response.headers.get("Content-Type")
    assert content_type is None, "Unexpected Content-Type: " + str(content_type)


# validate_response_time()
def validate_response_time(response, expected_time):
    assert response.elapsed.total_seconds() <= expected_time, "Response time exceeded: " + str(
        round(response.elapsed.total_seconds(), 1))


# validate_environment()
def validate_environment(response, expected_env):
    response_env = response.request.headers.get('env')
    assert response_env == expected_env, f"Test is not running in {expected_env} Environment"


# validate response is a dictionary
def validate_response_is_a_dictionary(json_response):
    assert isinstance(json_response, dict), "Unexpected response type: " + str(type(json_response))


# validate response is a list
def validate_response_is_a_list(json_response):
    assert isinstance(json_response, list), "Unexpected response type: " + str(type(json_response))


# Unauthorized user message validation
def validate_unauthenticated_user_message(response):
    assert response.json()['message'] == "Authentication failed", "Unexpected message for unauthenticated user: " + response.json()['message']


# Bad request message validation
def validate_bad_request_message(json_response):
    assert json_response['message'] == "Error occurred while parsing request parameters"\
        , "Unexpected bad request message" + json_response["message"]


# validate resource not found message
def validate_resource_not_found_message(response):
    assert response.json()['message'] == "Resource not found",\
        "Unexpected message displayed instead of Resource not found: " + response.json()['message']

# validate_single_object_schema()
def validate_single_object_schema(json_response, expected_schema):
    try:
        validate(instance=json_response, schema=expected_schema)
    except exceptions.ValidationError as ve:
        raise AssertionError("JSON data is invalid", ve)

# validate multiple objects schema
def validate_multiple_object_schema(json_response, expected_schema):
    # validating only 3 random objects in list as there could be many
    try:
        if len(json_response) == 0:
            raise AssertionError("Empty data is returned, Please prefer data that exist" )
        elif len(json_response) >= 10:
            items = random.sample(json_response, 3)
            for item in items:
                validate(instance=item, schema=expected_schema)
        else:
            for item in json_response:
                validate(instance=item, schema=expected_schema)
    except exceptions.ValidationError as ve:
        raise AssertionError("JSON data is invalid", ve)


# Function to handle 429 status code
def handle_too_many_request_429(response):
    if response.status_code == 429:
        retry_after = int(response.headers.get('X-RateLimit-Reset'))
        time.sleep(retry_after)
        print(f"Received 429 status code. Retrying after {retry_after} seconds.")
        raise requests.exceptions.RetryError(response=response)  # Raise RetryError to trigger the retry mechanism


