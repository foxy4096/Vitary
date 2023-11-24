import os
from django.http import JsonResponse


def get_routes(request):
    """
    Get the routes for the API
    """
    routes = [
        {
            'name': 'zen',
            'path': '/api/v1/zen/',
            'method': 'GET',
            'description': 'Get Zen, you will love it!',
            'required_login': False,
        },
        {
            'name': 'get_routes',
            'path': '/api/v1/',
            'method': 'GET',
            'description': 'Get the routes for the API',
            'required_login': False,
        },
        {
            'name': 'get_message_api',
            'path': '/api/v1/chat/get_message/',
            'method': 'GET',
            'description': 'Get the messages',
            'data': {
                'to_user': 'The username of the user you want to get the messages from',
            },
            'info': "This api url is not available to the public",
            'required_login': True,
        },
        {
            'name': 'send_message_api',
            'path': '/api/v1/chat/send_message/',
            'method': 'POST',
            'description': 'Send a message',
            'data': {
                'message': 'The message you want to send',
                'chat_id': 'The id of the chat you want to send the message to',
            },
            'info': "This api url is not avilable to the public",
            'required_login': True,
        },
        {
            'name': 'follow',
            'path': '/api/v1/follow/',
            'method': 'POST',
            'description': 'Follow a user',
            'data': {
                'username': 'The username of the user you want to follow',
            },
            'required_login': True,
        },
        {
            'name': 'user_view_api',
            'path': '/api/v1/user/',
            'method': 'GET',
            'description': 'Get a user',
            'data': {
                'username': 'The username of the user you want to get',
            },
            'required_login': True,
        },
        {
            'name': 'user_search_api',
            'path': '/api/v1/users/search/',
            'method': 'GET',
            'description': 'Search for a user',
            'data': {
                'query': 'The info of the user you want to search for',
            },
            'required_login': True,
        },
        {
            'name': 'like',
            'path': '/api/v1/feed/like/',
            'method': 'POST',
            'description': 'Like a feed',
            'data': {
                'feed_pk': 'The id of the feed you want to like',
            },
            'required_login': True,
        },
        {
            'name': 'get_feeds',
            'path': '/api/v1/feed/',
            'method': 'GET',
            'description': 'Get feeds',
            'required_login': True,

        },
        {
            'name': 'get_feed',
            'path': '/api/v1/feed/<int:id>/',
            'method': 'GET',
            'description': 'Get a feed',
            'required_login': True,
        },
        {
            'name': 'add_feed',
            'path': '/api/v1/feed/add/',
            'method': 'POST',
            'description': 'Add a feed',
            'data': {
                'body': 'The body of the feed you want to add',
            },
            'info': """
                    Currently uploading files is not supported.
                    """,
            'required_login': True,
        },
        {
            'name': 'edit_feed',
            'path': '/api/v1/feed/edit/',
            'method': 'POST',
            'description': 'Edit a feed',
            'data': {
                'feed_pk': 'The id of the feed you want to edit',
                'body': 'The body of the feed you want to edit',
            },
            'required_login': True,
        },
        {
            'name': 'delete_feed',
            'path': '/api/v1/feed/delete/',
            'method': 'POST',
            'description': 'Delete a feed',
            'data': {
                'feed_pk': 'The id of the feed you want to delete',
            },
            'required_login': True,
        }
    ]
    return JsonResponse(routes, safe=False, status=200)


def zen(request):
    """
    /api/v1/zen/ -> GET -> Returns the lyrics of Never Gonna Give You Up
    """
    module_dir = os.path.dirname(__file__)
    zen_txt = open(os.path.join(module_dir, 'zen.txt')).read()
    return JsonResponse({'zen': zen_txt})