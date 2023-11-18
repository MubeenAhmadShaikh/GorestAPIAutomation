import inspect
import logging


from utilities.confguraions import *
from utilities import urls
import requests

config = get_config()
qa_env = 'qa'
base_url = config['BASE_URL'][qa_env]
access_token = config['auth']['token']


class Base:

    def get_logger(self):
        logger_name = inspect.stack()[1][3]
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler("../logs/logging.log")
        fh.setFormatter(
            logging.Formatter("%(asctime)s -[%(filename)s:%(lineno)d] - [%(name)s] - [%(levelname)s] - %(message)s"))
        logger.handlers = []
        logger.addHandler(fh)
        return logger

    # common function for creating a new user
    def create_new_user(self):
        header = {'Authorization': f'Bearer {access_token}'}
        user_data = {
            "name": "Gustavo",
            "gender": "male",
            "email": "gas@email.com",
            "status": "active"
        }
        response = requests.post(base_url + urls.common_user_url(), data=user_data, headers=header)
        try:
            if response.status_code == 201:
                return response
            elif response.status_code == 422:
                response = self.search_user_by_email(user_data['email'])
                self.delete_existing_user(response.json()['id'])
        except AssertionError:
            raise "Unable to create new user"

    # common function for searching a user with email id
    def search_user_by_email(self, email):
        header = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(base_url + urls.search_user_by_email_url(email), headers=header)
        try:
            if response.status_code == 200:
                return response
        except AssertionError:
            raise "Unable to search user"

    # common function for deleting a user with user id
    def delete_existing_user(self, user_id):
        header = {'Authorization': f'Bearer {access_token}'}
        response = requests.delete(base_url + urls.single_user_url(user_id), headers=header)
        try:
            if response.status_code == 204:
                return 'User deleted successfully'
        except AssertionError:
            raise f"Unable to delete user with id {user_id}"

    # common function for returning a random user from api
    def get_a_random_user(self):
        response = requests.get(base_url + urls.common_user_url())
        try:
            if response.status_code == 200:
                random_user = response.json()[0]
                return random_user
        except AssertionError:
            raise f"Unable to get the users data"

    # common function for returning a random post from api
    def get_a_random_post(self):
        response = requests.get(base_url + urls.common_post_url())
        try:
            if response.status_code == 200:
                random_post = response.json()[0]
                return random_post
        except AssertionError:
            raise f"Unable to get the posts data"

    # common function for deleting a post with post id
    def delete_existing_post(self, post_id):
        header = {'Authorization': f'Bearer {access_token}'}
        response = requests.delete(base_url + urls.single_post_url(post_id), headers=header)
        try:
            if response.status_code == 204:
                return 'Post deleted successfully'
        except AssertionError:
            raise f"Unable to delete post with id {post_id}"
