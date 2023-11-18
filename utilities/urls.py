
def common_user_url():
    # This url can be used for POST and GET all users
    return f'users'


def single_user_url( user_id):
    # This url can be used for PUT, PATCH, DELETE and GET single user
    return f'users/{user_id}'


def search_user_by_name_url( name):
    # This url can be used to search the user by name
    return f'users?name={name}'


def search_user_by_email_url(email):
    # This url can be used to search the user by email
    return f'users?email={email}'


def search_user_with_pagination_url( page, per_page):
    return f'users?page={page}&per_page={per_page}'


def common_post_url():
    # This url can be used for POST and GET all posts
    return f'posts'


def single_post_url( post_id):
    # This url can be used for PUT, PATCH, DELETE and GET single posts
    return f'posts/{post_id}'


def search_post_by_title_url( title):
    # This url can be used to search the post by title
    return f'posts?title={title}'


def search_post_by_user_id_url( user_id):
    # This url can be used to search the post by user_id
    return f'posts?user_id={user_id}'


def search_post_by_body_url( body):
    # This url can be used to search the post by body description
    return f'posts?body={body}'


def search_post_with_pagination_url( page, per_page):
    return f'posts?page={page}&per_page={per_page}'