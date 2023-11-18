import pytest
from test_data.users_data import get_create_user_data_from_excel
from test_data.posts_data import get_create_post_data_from_excel


@pytest.fixture(params=get_create_user_data_from_excel())
def get_create_user_data(request):
    return request.param


@pytest.fixture(params=get_create_post_data_from_excel())
def get_create_post_data(request):
    return request.param