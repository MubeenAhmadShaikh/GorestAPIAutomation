import random

from jsonschema import validate, exceptions


# validate_empty_list_is_returned
def validate_empty_list_is_returned(json_response):
    assert len(json_response) == 0, "Users with entered data exist" + str(json_response)


# validate_response_body()
def validate_response_body(user_data, json_response):
    try:
        assert json_response['name'] == user_data['name']
        assert json_response['email'] == user_data['email']
        assert json_response['gender'] == user_data['gender']
        assert json_response['status'] == user_data['status']
    except AssertionError:
        raise AssertionError("Response data is not as expected")


# validate searched users name keywords are  present in names fields of returned objects
def validate_searched_user_by_name(json_response, searched_name):
    try:
        if len(json_response) >= 10:
            items = random.sample(json_response, 3)
            for item in items:
                assert searched_name in item['name'].lower()
        else:
            for item in json_response:
                assert searched_name in item['name'].lower()
    except exceptions.ValidationError as ve:
        raise AssertionError("searched name keywords are not present in all the users", ve)


# validate searched user email keywords are present in email fields of returned objects
def validate_searched_user_by_email(json_response, searched_email):
    try:
        if len(json_response) >= 10:
            items = random.sample(json_response, 3)
            for item in items:
                assert searched_email in item['email'].lower()
        else:
            for item in json_response:
                assert searched_email in item['email'].lower()
    except exceptions.ValidationError as ve:
        raise AssertionError("searched email keywords are not present in all the users", ve)


# validate per page returned objects are as expected
def validate_perpage_objects_length(json_response, per_page):
    assert len(json_response) == per_page, "Unexpected numbers of objects are returned"


# Invalid pagination validation
def validate_invalid_pagination(page, per_page):
    if isinstance(page, int) or isinstance(per_page, int):
        assert (page > 0 or per_page > 0), "[intentionally failed]No error message returned for invalid page: " + \
                                  str(page) + " with type as " + str(type(page))

    assert isinstance(page, int), "[intentionally failed]No error message returned for invalid page: " + \
                                  str(page) + " with type as " + str(type(page))
    assert isinstance(per_page, int), "[intentionally failed]No error message returned for invalid per_page: " +\
                                      str(per_page) + " with type as "+str(type(per_page))


# validate sending blank data
def validate_sending_blank_data(json_response):
    for item in json_response:
        if item['field'] == 'gender':
            assert item['message'] == "can't be blank, can be male of female"
        else:
            assert item['message'] == "can't be blank"


# validate duplicate email message
def validate_duplicate_email_message(json_response):
    for item in json_response:
        assert (item['field'] == "email" and item['message'] == "has already been taken")


# Invalid gender and email validation
def validate_invalid_gender_and_email(json_response):
    for item in json_response:
        if item['field'] == "gender":
            assert item['message'] == "can't be blank, can be male of female", "Unexpected invalid gender message: "+ item['message']
        else:
            assert item['message'] == "is invalid", "Unexpected invalid email message" + item['message']

# validate_error_handling()
