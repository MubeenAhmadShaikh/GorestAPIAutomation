
import pytest
import requests
from retrying import retry
from utilities.confguraions import *
from utilities.base import Base
from utilities import urls
from test_data import schemas
from utilities.fixtures import get_create_user_data
from utilities.validations import users_validations, common_validations


# config = get_config()
# qa_url = 'qa'
# base_url = config['BASE_URL'][qa_url]
# access_token = config['auth']['token']

# Initialize the configparser
config = configparser.ConfigParser()

# Load the configuration file
config.read('../conf.ini')  # Make sure to provide the correct path to your conf.ini file

# Get the environment (e.g., 'qa' or 'prod')
environment = 'qa'  # Change this to the desired environment

# Access the base URL based on the environment
base_url = config.get('BASE_URL', environment, fallback=None)
access_token = config.get('auth', 'token', fallback=None)




class TestUsers(Base):
    se = requests.session()
    se.headers.update({'Authorization': f'Bearer {access_token}'})
    se.headers.update({'env': 'qa'})
    # Positive Tests

    @pytest.mark.positive
    # Define a retry decorator with a strategy for retrying on 429 status code
    @retry(stop_max_attempt_number=3)
    def test_create_new_user_positive(self, get_create_user_data):
        """
        Validation points:
        - validate_successful_response_201
        - validate_content_type
        - validate_auth_token
        - validate response is a dictionary
        - validate_response_time
        - validate_environment
        - validate_single_object_schema
        - validate_response_body
        - validate gender is either male or female
        - validate status is either active or inactive
        """
        logs = self.get_logger()
        user_data = {
            "name": get_create_user_data['name'],
            "gender": get_create_user_data['gender'],
            "email": get_create_user_data['email'],
            "status": get_create_user_data['status']
        }
        expected_schema = schemas.single_user_schema()
        response = TestUsers.se.post(base_url+urls.common_user_url(), data=user_data)
        try:
            common_validations.validate_status_code(response, 201)
            logs.info("created new user successfully: status 201")
            data = response.json()
            common_validations.validate_content_type(response)
            common_validations.validate_auth_token(response, access_token)
            common_validations.validate_response_is_a_dictionary(data)
            common_validations.validate_response_time(response, 2.0)
            logs.info("response time taken: "+str(round(response.elapsed.total_seconds(), 1)))
            common_validations.validate_environment(response, "qa")
            common_validations.validate_single_object_schema(data, expected_schema)
            users_validations.validate_response_body(user_data, data)
            logs.info("validated user data successfully")
        except AssertionError as ae:
            logs.error(f"Test failed: {ae}")
            raise ae
        finally:
            if response.status_code == 201:
                self.delete_existing_user(response.json()['id'])

    @pytest.mark.positive
    @retry(stop_max_attempt_number=3)
    def test_get_user_by_id_positive(self):
        """
        Validation points:
        - validate_successful_response_200
        - validate_content_type
        - validate_auth_token
        - validate response is a dictionary
        - validate_response_time
        - validate_environment
        - validate_single_object_schema
        - validate_response_body
        """
        logs = self.get_logger()
        random_user_response = self.get_a_random_user()
        user_id = random_user_response['id']
        expected_schema = schemas.single_user_schema()
        response = TestUsers.se.get(base_url + urls.single_user_url(user_id))
        try:
            common_validations.validate_status_code(response, 200)
            data = response.json()
            logs.info(f"getting single user by id {user_id} successfully")
            assert data['id'] == user_id, "Unexpected data is returned" + data
            logs.info("validated user data successfully")
            common_validations.validate_content_type(response)
            common_validations.validate_auth_token(response, access_token)
            logs.info("validated Auth token successfully")
            common_validations.validate_response_is_a_dictionary(data)
            common_validations.validate_response_time(response, 2.0)
            logs.info("response time taken: " + str(round(response.elapsed.total_seconds(), 1)))
            common_validations.validate_environment(response, "qa")
            common_validations.validate_single_object_schema(data, expected_schema)
        except AssertionError as ae:
            logs.error(f"Test failed: {ae}")
            raise ae

    @pytest.mark.positive
    @retry(stop_max_attempt_number=3)
    def test_get_all_users_positive(self):
        """
        Validation points:
        - validate_successful_response_200
        - validate_content_type
        - validate_auth_token
        - validate response is an array/list
        - validate_response_time
        - validate_environment
        - validate_multiple_object_schema
        """
        logs = self.get_logger()
        expected_schema = schemas.single_user_schema()
        response = TestUsers.se.get(base_url + urls.common_user_url())
        try:
            common_validations.validate_status_code(response, 200)
            data = response.json()
            logs.info("getting all the user successfully: status 200")
            common_validations.validate_content_type(response)
            common_validations.validate_auth_token(response, access_token)
            common_validations.validate_response_is_a_list(data)
            common_validations.validate_response_time(response, 2.0)
            common_validations.validate_environment(response, "qa")
            common_validations.validate_multiple_object_schema(data, expected_schema)
        except AssertionError as ae:
            logs.error(f"Test failed: {ae}")
            raise ae

    @pytest.mark.positive
    @retry(stop_max_attempt_number=3)
    def test_search_users_by_name_positive(self):
        logs = self.get_logger()
        expected_schema = schemas.single_user_schema()
        user_name = 'kan'  # kamla
        response = TestUsers.se.get(base_url + urls.search_user_by_name_url(user_name))
        try:
            common_validations.validate_status_code(response, 200)
            data = response.json()
            logs.info(f"searched user by name {user_name} successfully: status 200")
            users_validations.validate_searched_user_by_name(data, user_name)
            logs.info("validated searched user successfully")
            common_validations.validate_content_type(response)
            common_validations.validate_auth_token(response, access_token)
            common_validations.validate_response_is_a_list(data)
            common_validations.validate_response_time(response, 2.0)
            common_validations.validate_environment(response, "qa")
            common_validations.validate_multiple_object_schema(data, expected_schema)
        except AssertionError as ae:
            logs.error(f"Test failed: {ae}")
            raise ae

    @pytest.mark.positive
    @retry(stop_max_attempt_number=3)
    def test_search_users_by_email_positive(self):
        logs = self.get_logger()
        expected_schema = schemas.single_user_schema()
        user_email = 'kan'  # com
        response = TestUsers.se.get(base_url + urls.search_user_by_email_url(user_email))
        try:
            common_validations.validate_auth_token(response, access_token)
            common_validations.validate_status_code(response, 200)
            data = response.json()
            logs.info(f"searched user by email {user_email} successfully: status 200")
            users_validations.validate_searched_user_by_email(data, user_email)
            logs.info("validated searched user successfully")
            common_validations.validate_multiple_object_schema(data, expected_schema)
            common_validations.validate_response_is_a_list(data)
            common_validations.validate_content_type(response)
            common_validations.validate_response_time(response, 2.0)
            common_validations.validate_environment(response, "qa")
        except AssertionError as ae:
            logs.error(f"Test failed: {ae}")
            raise ae

    @pytest.mark.positive
    @retry(stop_max_attempt_number=3)
    def test_search_user_pagination_positive(self):
        logs = self.get_logger()
        expected_schema = schemas.single_user_schema()
        page = 3
        per_page = 5
        response = TestUsers.se.get(base_url + urls.search_user_with_pagination_url(page, per_page))
        try:
            common_validations.validate_status_code(response, 200)
            data = response.json()
            logs.info(f"searched using pagination parameters page {page} and per page {per_page} successfully: status 200")
            users_validations.validate_perpage_objects_length(data, per_page)
            logs.info("validated page and its returned items length.")
            common_validations.validate_content_type(response)
            common_validations.validate_auth_token(response, access_token)
            common_validations.validate_response_is_a_list(data)
            common_validations.validate_response_time(response, 2.0)
            common_validations.validate_environment(response, "qa")
            common_validations.validate_multiple_object_schema(data, expected_schema)
        except AssertionError as ae:
            logs.error(f"Test failed: {ae}")
            raise ae

    @pytest.mark.positive
    @retry(stop_max_attempt_number=3)
    def test_update_user_positive(self, get_create_user_data):
        logs = self.get_logger()
        random_user_response = self.get_a_random_user()
        user_id = random_user_response['id']
        user_update_data = {
            "name": get_create_user_data['name'],
            "email": get_create_user_data['email'],
            "gender": get_create_user_data['gender'],
            "status": get_create_user_data['status']
        }
        response = TestUsers.se.put(base_url + urls.single_user_url(user_id), data=user_update_data)
        expected_schema = schemas.single_user_schema()
        try:
            common_validations.validate_status_code(response, 200)
            data = response.json()
            logs.info("updated existing user successfully: status 200")
            common_validations.validate_content_type(response)
            common_validations.validate_auth_token(response, access_token)
            common_validations.validate_response_is_a_dictionary(data)
            common_validations.validate_response_time(response, 2.0)
            common_validations.validate_environment(response, "qa")
            common_validations.validate_single_object_schema(data, expected_schema)
            users_validations.validate_response_body(user_update_data, data)
            logs.info("validated updated body response")
        except AssertionError as ae:
            logs.error(f"Test failed: {ae}")
            raise ae
        finally:
            if response.status_code == 200:
                self.delete_existing_user(user_id)

    @pytest.mark.positive
    @retry(stop_max_attempt_number=3)
    def test_delete_user_positive(self):
        logs = self.get_logger()
        random_user_response = self.get_a_random_user()
        user_id = random_user_response['id']
        response = TestUsers.se.delete(base_url + urls.single_user_url(user_id))
        try:
            common_validations.validate_status_code(response, 204)
            logs.info("deleted existing user successfully: status 204")
            common_validations.validate_none_content_type(response)
            common_validations.validate_auth_token(response, access_token)
            common_validations.validate_response_time(response, 2.0)
            common_validations.validate_environment(response, "qa")
        except AssertionError as ae:
            logs.error(f"Test failed: {ae}")
            raise ae

    # Negative Tests

    @pytest.mark.negative
    def test_create_new_user_negative(self):
        """
        Validation points:
        Note: For each '-' scenario different API request is sent as we have to differ the data in every request

        - Unauthorized user validation
            + validate unauthenticated status 401
            + validate unauthenticated user message
        - Blank request data validation [empty strings]
            + validate unprocessable entity 422
            + validate error messages for sending blank data
        - Duplicate email validation
            + validate unprocessable entity 422
            + validate duplicate email message
        - Invalid gender and email validation
            + validate unprocessable entity 422
            + validate error messages for sending invalid email and gender
        """
        logs = self.get_logger()
        # unauthenticated user validation
        try:
            user_data = {
                "name": "Gustavo",
                "gender": "male",
                "email": "gas@email.com",
                "status": "active"
            }
            response = requests.post(base_url + urls.common_user_url(), data=user_data)
            common_validations.validate_status_code(response, 401)
            common_validations.validate_unauthenticated_user_message(response)
            logs.info("[for unauthenticated user] Expected status code and messages are returned")
        except AssertionError as ae:
            logs.error(f"Test Failed:  {ae}")
            raise ae

        # sending blank data validation
        try:
            users_data = {
                "name": "",
                "gender": "",
                "email": "",
                "status": ""
            }
            response = TestUsers.se.post(base_url + urls.common_user_url(), data=users_data)
            common_validations.validate_status_code(response, 422)
            data = response.json()
            users_validations.validate_sending_blank_data(data)
            logs.info("[for blank data] Expected status code and messages are returned ")
        except AssertionError as ae:
            logs.error(f"Test Failed:  {ae}")
            raise ae

        # duplicate email validation
        random_user_response = self.get_a_random_user()
        try:
            duplicate_email = random_user_response['email']
            user_data = {
                "name": "Gustavo",
                "email": duplicate_email,
                "status": "active",
                "gender": "male"
            }
            response = TestUsers.se.post(base_url + urls.common_user_url(), data=user_data)
            common_validations.validate_status_code(response, 422)
            data = response.json()
            users_validations.validate_duplicate_email_message(data)
            logs.info("[for duplicate email] Expected status code and messages are returned ")
        except AssertionError as ae:
            logs.error(f"Test Failed:  {ae}")
            raise ae

        # invalid gender and email validation
        try:
            user_data = {
                "name": "Gustavo",
                "email": ".com",
                "status": "active",
                "gender": "other"
            }
            response = TestUsers.se.post(base_url + urls.common_user_url(), data=user_data)
            common_validations.validate_status_code(response, 422)
            data = response.json()
            users_validations.validate_invalid_gender_and_email(data)
            logs.info("[for invalid gender and email] Expected status code and messages are returned")
        except AssertionError as ae:
            logs.error(f"Test Failed:  {ae}")
            raise ae

    @pytest.mark.negative
    @pytest.mark.parametrize('invalid_user_id', [-123, "%$#@!", " "])
    def test_get_user_by_id_negative(self, invalid_user_id):
        # validate message
        logs = self.get_logger()
        response = TestUsers.se.get(base_url + urls.single_user_url(invalid_user_id))
        try:
            common_validations.validate_status_code(response, 404)
            common_validations.validate_resource_not_found_message(response)
            logs.info(f"[for invalid user_id {invalid_user_id}] Expected status code and messages are returned ")
        except AssertionError as ae:
            logs.error(f"Test Failed: {ae}")
            raise ae

    @pytest.mark.negative
    def test_search_users_by_name_negative(self):
        logs = self.get_logger()
        user_name = "azx"  # kan
        response = TestUsers.se.get(base_url + urls.search_user_by_name_url(user_name))
        try:
            common_validations.validate_status_code(response, 200)
            data = response.json()
            common_validations.validate_response_is_a_list(data)
            users_validations.validate_empty_list_is_returned(data)
            logs.info("[for searching invalid name user_name] Expected status code and messages are returned")
        except AssertionError as ae:
            logs.error(f"Test Failed: {ae}")
            raise ae

    @pytest.mark.negative
    def test_search_users_by_email_negative(self):
        logs = self.get_logger()
        user_email = "azx"  # kan
        response = TestUsers.se.get(base_url + urls.search_user_by_email_url(user_email))
        try:
            common_validations.validate_status_code(response, 200)
            data = response.json()
            common_validations.validate_response_is_a_list(data)
            users_validations.validate_empty_list_is_returned(data)
            logs.info(f"[for searching invalid email {user_email}] Expected status code and messages are returned")
        except AssertionError as ae:
            logs.error(f"Test Failed: {ae}")
            raise ae

    @pytest.mark.negative
    @pytest.mark.xfail
    @pytest.mark.parametrize('invalid_data', [-123, "%$#@!", " "])
    def test_search_user_pagination_negative(self, invalid_data):
        logs = self.get_logger()
        page = invalid_data
        per_page = invalid_data
        logs.info(f"Page provided: {page} per_page: {per_page}")
        response = TestUsers.se.get(base_url + urls.search_user_with_pagination_url(page, per_page))
        try:
            common_validations.validate_status_code(response, 200)
            users_validations.validate_invalid_pagination(page, per_page)
            logs.info("Expected status code and messages are returned for searching invalid pagination parameters")
        except AssertionError as ae:
            logs.error(f"Test Failed: {ae}")
            raise ae

    @pytest.mark.negative
    def test_update_user_negative(self):
        logs = self.get_logger()
        # unauthenticated user validation
        get_user_response = self.get_a_random_user()
        try:
            user_data = {
                "name": "Gustavo",
                "email": "gas@email.com",
                "status": "active"
            }
            response = requests.put(base_url + urls.single_user_url(get_user_response['id']), data=user_data)
            common_validations.validate_status_code(response, 401)
            common_validations.validate_unauthenticated_user_message(response)
            logs.info("[for updating unauthenticated user] Expected status code and messages are returned")
        except AssertionError as ae:
            logs.error(f"Test Failed: {ae}")
            raise ae

        # sending blank data validation
        try:
            users_data = {
                "name": "",
                "gender": "",
                "status": ""
            }
            response = TestUsers.se.put(base_url + urls.single_user_url(get_user_response['id']), data=users_data)
            common_validations.validate_status_code(response, 422)
            data = response.json()
            users_validations.validate_sending_blank_data(data)
            logs.info("[for updating blank data] Expected status code and messages are returned")
        except AssertionError as ae:
            logs.error(f"Test Failed: {ae}")
            raise ae

        # duplicate email validation
        try:
            duplicate_email = get_user_response['email']
            user_data = {
                "name": "joke",
                "email": duplicate_email,
                "status": "active",
                "gender": "male"
            }
            response = TestUsers.se.post(base_url + urls.common_user_url(), data=user_data)
            common_validations.validate_status_code(response, 422)
            data = response.json()
            users_validations.validate_duplicate_email_message(data)
            logs.info(f"[for updating duplicate email {duplicate_email}] Expected status code and messages are returned")
        except AssertionError as ae:
            logs.error(f"Test Failed: {ae}")
            raise ae

        # invalid gender and email validation
        try:
            user_data = {
                "name": "Gustavo",
                "status": "active",
                "email": ".com",
                "gender": "other"
            }
            response = TestUsers.se.post(base_url + urls.common_user_url(), data=user_data)
            common_validations.validate_status_code(response, 422)
            data = response.json()
            users_validations.validate_invalid_gender_and_email(data)
            logs.info("[for updating invalid gender and email] Expected status code and messages are returned ")
        except AssertionError as ae:
            logs.error(f"Test Failed: {ae}")
            raise ae

    @pytest.mark.negative
    def test_delete_user_negative(self):
        logs = self.get_logger()
        # unauthenticated user validation
        get_user_response = self.get_a_random_user()
        try:
            user_id = get_user_response['id']
            response = requests.delete(base_url + urls.single_user_url(user_id))
            common_validations.validate_status_code(response, 401)
            common_validations.validate_unauthenticated_user_message(response)
            logs.info("[for deleting unauthenticated user] Expected status code and messages are returned")
        except AssertionError as ae:
            logs.error(f"Test Failed: {ae}")
            raise ae

        # invalid user id
        try:
            user_id = 1
            response = TestUsers.se.delete(base_url + urls.single_user_url(user_id))
            common_validations.validate_status_code(response, 404)
            common_validations.validate_resource_not_found_message(response)
            logs.info("[for deleting with invalid user_id] Expected status code and messages are returned")
        except AssertionError as ae:
            logs.error(f"Test Failed: {ae}")
            raise ae
