import pytest
from retrying import retry
from utilities.base import Base
from utilities import urls
import requests
from test_data import schemas
from utilities.confguraions import *
from utilities.validations import common_validations, posts_validations, users_validations
from utilities.fixtures import get_create_post_data
# config = get_config()
# qa_env = 'qa'
# base_url = config['BASE_URL'][qa_env]
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


class TestPosts(Base):

    se = requests.session()
    se.headers.update({'Authorization': f'Bearer {access_token}'})

    # Positive Tests

    @pytest.mark.positive
    def test_create_new_post_positive(self, get_create_post_data):
        logs = self.get_logger()
        random_user_response = self.get_a_random_user()
        post_data = {
            "user_id": random_user_response['id'],
            "title": get_create_post_data['title'],
            "body": get_create_post_data['body'],
        }
        expected_schema = schemas.single_post_schema()
        response = TestPosts.se.post(base_url + urls.common_post_url(), data=post_data)
        try:
            common_validations.validate_status_code(response, 201)
            logs.info("created new post successfully: status 201")
            data = response.json()
            common_validations.validate_content_type(response)
            common_validations.validate_auth_token(response, access_token)
            common_validations.validate_response_is_a_dictionary(data)
            common_validations.validate_response_time(response, 1)
            logs.info("response time taken: " + str(round(response.elapsed.total_seconds(), 1)))
            common_validations.validate_single_object_schema(data, expected_schema)
            posts_validations.validate_post_response_body(post_data, data)
            logs.info("validated post data successfully")
        except AssertionError as ae:
            logs.error(f"Test Failed while creating new post {ae}")
            pytest.fail(f"Test Failed while creating new post {ae}")

    @pytest.mark.positive
    def test_get_post_by_id_positive(self):
        logs = self.get_logger()
        random_post_response = self.get_a_random_post()
        post_id = random_post_response['id']
        expected_schema = schemas.single_post_schema()
        response = TestPosts.se.get(base_url + urls.single_post_url(post_id))
        try:
            common_validations.validate_status_code(response, 200)
            logs.info(f"getting single post by id {post_id} successfully")
            data = response.json()
            assert data['id'] == post_id, "Unexpected data is returned" + data
            logs.info("validated post data successfully")
            common_validations.validate_content_type(response)
            common_validations.validate_auth_token(response, access_token)
            common_validations.validate_response_is_a_dictionary(data)
            common_validations.validate_response_time(response, 2.0)
            common_validations.validate_single_object_schema(data, expected_schema)
        except AssertionError as ae:
            logs.error(f"Test Failed while getting post by id {ae}")
            pytest.fail(f"Test Failed while getting post by id {ae}")

    @pytest.mark.positive
    def test_get_all_posts_positive(self):
        logs = self.get_logger()
        expected_schema = schemas.single_post_schema()
        response = TestPosts.se.get(base_url + urls.common_post_url())
        try:
            common_validations.validate_status_code(response, 200)
            data = response.json()
            logs.info("getting all the posts successfully: status 200")
            common_validations.validate_content_type(response)
            common_validations.validate_auth_token(response, access_token)
            common_validations.validate_response_is_a_list(data)
            common_validations.validate_response_time(response, 1.0)
            common_validations.validate_multiple_object_schema(data, expected_schema)
        except AssertionError as ae:
            logs.error(f"Test Failed while getting all posts {ae}")
            pytest.fail(f"Test Failed while getting all posts {ae}")

    @pytest.mark.positive
    def test_search_post_by_title_positive(self):
        logs = self.get_logger()
        expected_schema = schemas.single_post_schema()
        random_post_response = self.get_a_random_post()
        post_title = random_post_response['title'][0:5].lower()
        response = TestPosts.se.get(base_url + urls.search_post_by_title_url(post_title))
        try:
            common_validations.validate_status_code(response, 200)
            data = response.json()
            logs.info(f"searched post by title {post_title} successfully: status 200")
            posts_validations.validate_searched_post_by_title(data, post_title)
            logs.info("validated searched post successfully")
            common_validations.validate_content_type(response)
            common_validations.validate_auth_token(response, access_token)
            common_validations.validate_response_is_a_list(data)
            common_validations.validate_response_time(response, 1.0)
            common_validations.validate_multiple_object_schema(data, expected_schema)
        except AssertionError as ae:
            logs.error(f"Test Failed while searching post by title positive {ae}")
            pytest.fail(f"Test Failed while searching post by title positive {ae}")

    @pytest.mark.positive
    def test_search_post_by_body_positive(self):
        logs = self.get_logger()
        expected_schema = schemas.single_post_schema()
        random_post_response = self.get_a_random_post()
        post_body = random_post_response['body'][0:5].lower()
        response = TestPosts.se.get(base_url + urls.search_post_by_body_url(post_body))
        try:
            common_validations.validate_status_code(response, 200)
            data = response.json()
            logs.info(f"searched post by body {post_body} successfully: status 200")
            posts_validations.validate_searched_post_by_body(data, post_body)
            logs.info("validated searched post successfully")
            common_validations.validate_content_type(response)
            common_validations.validate_auth_token(response, access_token)
            common_validations.validate_response_is_a_list(data)
            common_validations.validate_response_time(response, 1.0)
            common_validations.validate_multiple_object_schema(data, expected_schema)
        except AssertionError as ae:
            logs.error(f"Test Failed while searching post by body positive {ae}")
            pytest.fail(f"Test Failed while searching post by body positive {ae}")

    @pytest.mark.positive
    def test_search_post_by_user_id_positive(self):
        logs = self.get_logger()
        expected_schema = schemas.single_post_schema()
        random_user_response = self.get_a_random_user()
        user_id = random_user_response['id']
        response = TestPosts.se.get(base_url + urls.search_post_by_user_id_url(user_id))
        try:
            common_validations.validate_status_code(response, 200)
            data = response.json()
            logs.info(f"searched post by user_id {user_id} successfully: status 200")
            posts_validations.validate_searched_post_by_user_id(data, user_id)
            logs.info("validated searched post using user_id successfully")
            common_validations.validate_content_type(response)
            common_validations.validate_auth_token(response, access_token)
            common_validations.validate_response_is_a_list(data)
            common_validations.validate_response_time(response, 1.0)
            common_validations.validate_multiple_object_schema(data, expected_schema)
        except AssertionError as ae:
            logs.error(f"Test Failed while searching post by user_id positive {ae}")
            pytest.fail(f"Test Failed while searching post by user_id positive {ae}")

    @pytest.mark.positive
    def test_pagination_positive(self):
        logs = self.get_logger()
        expected_schema = schemas.single_post_schema()
        page = 3
        per_page = 20
        response = TestPosts.se.get(base_url + urls.search_post_with_pagination_url(page, per_page))
        try:
            common_validations.validate_status_code(response, 200)
            data = response.json()
            logs.info(f"searched using pagination parameters page {page} and per page {per_page}"
                      f" successfully: status 200")
            users_validations.validate_perpage_objects_length(data, per_page)
            logs.info("validated page and its returned items length.")
            common_validations.validate_content_type(response)
            common_validations.validate_auth_token(response, access_token)
            common_validations.validate_response_is_a_list(data)
            common_validations.validate_response_time(response, 1.0)
            common_validations.validate_multiple_object_schema(data, expected_schema)
        except AssertionError as ae:
            logs.error(f"Test Failed during pagination positive {ae}")
            pytest.fail(f"Test Failed during pagination positive {ae}")

    @pytest.mark.positive
    def test_update_post_positive(self, get_create_post_data):
        logs = self.get_logger()
        random_post_response = self.get_a_random_post()
        user_id = random_post_response['user_id']
        post_id = random_post_response['id']
        post_update_data = {
            "user_id": user_id,
            "title": get_create_post_data['title'],
            "body": get_create_post_data['body'],
        }
        response = TestPosts.se.put(base_url + urls.single_post_url(post_id), data=post_update_data)
        expected_schema = schemas.single_post_schema()
        try:
            common_validations.validate_status_code(response, 200)
            data = response.json()
            logs.info("updated existing post successfully: status 200")
            common_validations.validate_content_type(response)
            common_validations.validate_auth_token(response, access_token)
            common_validations.validate_response_is_a_dictionary(data)
            common_validations.validate_response_time(response, 2.0)
            common_validations.validate_single_object_schema(data, expected_schema)
            posts_validations.validate_post_response_body(post_update_data, data)
            logs.info("validated updated body response")
        except AssertionError as ae:
            logs.error(f"Test Failed while updating post positive {ae}")
            pytest.fail(f"Test Failed while updating post positive {ae}")

    @pytest.mark.positive
    def test_delete_post_positive(self):
        logs = self.get_logger()
        random_post_response = self.get_a_random_post()
        post_id = random_post_response['id']
        response = TestPosts.se.delete(base_url + urls.single_post_url(post_id))
        try:
            common_validations.validate_status_code(response, 204)
            logs.info("deleted existing post successfully: status 204")
            common_validations.validate_none_content_type(response)
            common_validations.validate_auth_token(response, access_token)
            common_validations.validate_response_time(response, 1.0)
        except AssertionError as ae:
            logs.error(f"Test Failed while deleting post positive {ae}")
            pytest.fail(f"Test Failed while deleting post positive {ae}")

    # Negative Tests

    @pytest.mark.negative
    def test_create_new_post_negative(self):
        logs = self.get_logger()
        # Unauthenticated user
        try:
            post_data = {
                "title": "random post",
                "body": "post description",
                "user_id": 1
            }
            response = requests.post(base_url + urls.common_post_url(), data=post_data)
            common_validations.validate_status_code(response, 401)
            common_validations.validate_unauthenticated_user_message(response)
            logs.info("[for unauthenticated user] Expected status code and messages are returned")
        except AssertionError as ae:
            logs.error(f"Test Failed for creating new post negative[Unauthenticated user] {ae}")
            pytest.fail(f"Test Failed for creating new post negative[Unauthenticated user] {ae}")

        # sending blank data validation
        try:
            post_data = {
                "title": "",
                "body": "",
                "user_id": ""
            }
            response = TestPosts.se.post(base_url + urls.common_post_url(), data=post_data)
            common_validations.validate_status_code(response, 422)
            data = response.json()
            posts_validations.validate_sending_blank_data(data)
        except AssertionError as ae:
            logs.error(f"Test Failed for creating new post negative[Blank data] {ae}")
            pytest.fail(f"Test Failed for creating new post negative[Blank data] {ae}")

        # non-existent user_id [string, special characters]
        try:
            post_data = {
                "title": "",
                "body": "",
                "user_id": 1
            }
            response = TestPosts.se.post(base_url + urls.common_post_url(), data=post_data)
            common_validations.validate_status_code(response, 422)
            logs.info(f"[for non-existent user_id 1] Expected status code and messages are returned ")
            data = response.json()
            posts_validations.validate_sending_blank_data(data)
        except AssertionError as ae:
            logs.error(f"Test Failed for creating new post negative[non-existent user] {ae}")
            pytest.fail(f"Test Failed for creating new post negative[non-existent user] {ae}")

    @pytest.mark.negative
    @pytest.mark.parametrize('invalid_post_id', [-123, "%$#@!", " "])
    def test_get_post_by_id_negative(self, invalid_post_id):
        logs = self.get_logger()
        response = TestPosts.se.get(base_url + urls.single_post_url(invalid_post_id))
        try:
            common_validations.validate_status_code(response, 404)
            common_validations.validate_resource_not_found_message(response)
            logs.info(f"[for invalid post_id {invalid_post_id}] Expected status code and messages are returned ")
        except AssertionError as ae:
            logs.error(f"Test Failed for getting post by id negative{ae}")
            pytest.fail(f"Test Failed for getting post by id negative{ae}")

    @pytest.mark.negative
    def test_search_post_by_title_negative(self):
        # This cannot be tested as it returns the values because post titles accept any value inside strings
        pass

    @pytest.mark.negative
    def test_search_post_by_user_id_negative(self):
        # This cannot be tested as it returns the values because post body accept any value inside strings
        pass

    @pytest.mark.negative
    @pytest.mark.xfail
    @pytest.mark.parametrize('invalid_data', [-123, "%$#@!", " "])
    @retry(stop_max_attempt_number=3, retry_on_result=lambda result: result == 429)
    def test_pagination_negative(self, invalid_data):
        logs = self.get_logger()
        page = invalid_data
        per_page = invalid_data
        response = TestPosts.se.get(base_url + urls.search_post_with_pagination_url(page, per_page))
        logs.info(f"Page provided: {page} per_page: {per_page}")
        try:
            common_validations.validate_status_code(response, 200)
            users_validations.validate_invalid_pagination(page, per_page)
            logs.info("Expected status code and messages are returned for searching invalid pagination parameters")
        except AssertionError as ae:
            if response.status_code == 429:
                logs.warning("Retrying due to status code 429 Too many requests")
                return 429  # This triggers a retry for status code 429
            logs.error(f"Test Failed during pagination negative{ae}")
            pytest.fail(f"Test Failed during pagination negative{ae}")

    @pytest.mark.negative
    def test_update_post_negative(self):
        logs = self.get_logger()
        # Unauthenticated user
        random_post_response = self.get_a_random_post()
        post_id = random_post_response['id']
        try:
            post_data = {
                "title": "random post",
                "body": "post description",
                "user_id": 1
            }
            response = requests.put(base_url + urls.single_post_url(post_id), data=post_data)
            common_validations.validate_status_code(response, 401)
            common_validations.validate_unauthenticated_user_message(response)
            logs.info("[for updating post with unauthenticated user] Expected status code and messages are returned")
        except AssertionError as ae:
            logs.error(f"Test Failed for creating new post negative[Unautneticated user] {ae}")
            pytest.fail(f"Test Failed for creating new post negative[Unautneticated user] {ae}")

        # sending blank data validation
        try:
            post_data = {
                "title": "",
                "body": "",
                "user_id": ""
            }
            response = TestPosts.se.put(base_url + urls.single_post_url(post_id), data=post_data)
            common_validations.validate_status_code(response, 422)
            data = response.json()
            posts_validations.validate_sending_blank_data(data)
            logs.info("[for updating with blank data] Expected status code and messages are returned")
        except AssertionError as ae:
            logs.error(f"Test Failed for updating post negative[Blank data] {ae}")
            pytest.fail(f"Test Failed for updating post negative[Blank data] {ae}")

        # non-existent user_id [string, special characters]
        try:
            post_data = {
                "title": "",
                "body": "",
                "user_id": 1
            }
            response = TestPosts.se.put(base_url + urls.single_post_url(post_id), data=post_data)
            common_validations.validate_status_code(response, 422)
            data = response.json()
            posts_validations.validate_sending_blank_data(data)
            logs.info(f"[for updating post with invalid user_id] Expected status code and messages are returned")
        except AssertionError as ae:
            logs.error(f"Test Failed for creating new post negative[non-existent user] {ae}")
            pytest.fail(f"Test Failed for creating new post negative[non-existent user] {ae}")

    @pytest.mark.negative
    @pytest.mark.parametrize('invalid_data', [-123, "!@#$"])
    def test_delete_post_negative(self, invalid_data):
        logs = self.get_logger()
        # unauthenticated user validation
        random_post_response = self.get_a_random_post()
        try:
            post_id = random_post_response['id']
            response = requests.delete(base_url + urls.single_post_url(post_id))
            common_validations.validate_status_code(response, 401)
            common_validations.validate_unauthenticated_user_message(response)
            logs.info("[for deleting post with unauthenticated user] Expected status code and messages are returned")
        except AssertionError as ae:
            logs.error(f"Test Failed for deleting post negative[Unautneticated user] {ae}")
            pytest.fail(f"Test Failed for deleting post negative[Unautneticated user] {ae}")

        # invalid user id
        try:
            response = TestPosts.se.delete(base_url + urls.single_post_url(invalid_data))
            common_validations.validate_status_code(response, 404)
            common_validations.validate_resource_not_found_message(response)
            logs.info("[for deleting post with invalid user_id] Expected status code and messages are returned")
        except AssertionError as ae:
            logs.error(f"Test Failed for creating new post negative[Invalid user] {ae}")
            pytest.fail(f"Test Failed for creating new post negative[Invalid user] {ae}")
