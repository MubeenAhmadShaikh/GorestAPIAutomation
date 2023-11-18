from jsonschema import validate, exceptions
import random

def validate_post_response_body(post_data, json_response):
    try:
        assert json_response['user_id'] == post_data['user_id']
        assert json_response['title'] == post_data['title']
        assert json_response['body'] == post_data['body']
    except AssertionError:
        raise AssertionError("Post Response data is not as expected")


def validate_single_post_schema(json_response, expected_schema):
    try:
        validate(instance=json_response, schema=expected_schema)
    except exceptions.ValidationError as ve:
        raise AssertionError("JSON data is invalid", ve)


def validate_searched_post_by_title(json_response, searched_title):
    try:
        if len(json_response) == 0:
            raise AssertionError("Empty data is returned, Please prefer data that exist")
        elif len(json_response) >= 10:
            items = random.sample(json_response, 3)
            for item in items:
                assert searched_title in item['title'].lower()
        else:
            for item in json_response:
                assert searched_title in item['title'].lower()
    except exceptions.ValidationError as ve:
        raise AssertionError("searched title keywords are not present in all the posts", ve)


def validate_searched_post_by_body(json_response, searched_body):
    try:
        if len(json_response) == 0:
            raise AssertionError("Empty data is returned, Please prefer data that exist")
        elif len(json_response) >= 10:
            items = random.sample(json_response, 3)
            for item in items:
                assert searched_body.lower() in item['body'].lower()
        else:
            for item in json_response:
                assert searched_body.lower() in item['body'].lower()
    except exceptions.ValidationError as ve:
        raise AssertionError("searched body keywords are not present in all the posts", ve)


def validate_searched_post_by_user_id(json_response, searched_user_id):
    try:
        if len(json_response) == 0:
            raise AssertionError("Empty data is returned, Please prefer data that exist")
        elif len(json_response) >= 10:
            items = random.sample(json_response, 3)
            for item in items:
                assert searched_user_id == item['user_id']
        else:
            for item in json_response:
                assert searched_user_id == item['user_id']
    except exceptions.ValidationError as ve:
        raise AssertionError("searched user_id user does not have any posts", ve)


def validate_sending_blank_data(json_response):
    for item in json_response:
        if item['field'] == 'user':
            assert item['message'] == "must exist", "blank user field message is unexpected: "+item['message']
        elif item['field'] == 'user_id':
            assert item['message'] == "is not a number", "user_id error message is unexpected: "+item['message']
        else:
            assert item['message'] == "can't be blank", "blank title/body field message is unexpected: "+item['message']