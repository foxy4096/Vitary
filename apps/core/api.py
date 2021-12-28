from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.urls import reverse


@api_view(['GET'])
def get_routes(request):
    routes = [
        {
            "Endpoint": "/api/v1/chat/get_message/?to_user=<str:to_user__username>",
            "Method": "GET",
            "Description": "Get messages",
            "Body": None,
        },
        {
            "Endpoint": "/api/v1/chat/send_message/",
            "Method": "POST",
            "Description": "Send message",
            "Body": {
                "to_user": "<str:to_user__username>",
                "body": "<str:body>",
                "chat_id": "<int:chat_id>",
            },
        },
        {
            "Endpoint": "api/v1/vit/",
            "Method": "GET",
            "Description": "Get Vits",
            "Body": None,
        },
        {
            "Endpoint": "/api/v1/vit/add_like/?vit_pk=<int:vit_pk>",
            "Method": "GET",
            "Description": "Add like",
            "Body": {
                "vit_pk": "<int:vit_pk>",
            }
        },
        {
            "Endpoint": "/api/v1/vit/<vit_pk>/",
            "Method": "GET",
            "Description": "Get Vit",
            "Body": {
                "vit_pk": "<int:vit_pk>",
            }
        },
        {
            "Endpoint": "/api/v1/vit/add/",
            "Method": "POST",
            "Description": "Add Vit",
            "Body": {
                "body": "<str:body>",
            },
        },
        {
            "Endpoint": "/api/v1/vit/edit/<vit_pk>/",
            "Method": "PUT",
            "Description": "Edit Vit",
            "Body": {
                "body": "<str:body>",
                
            }
        },
        {
            "Endpoint": "/api/v1/vit/<vit_pk>/delete/",
            "Method": "DELETE",
            "Description": "Delete Vit",
            "Body": {
                "vit_pk": "<int:vit_pk>",
            }
        },
        {
            "Endpoint": "api/v1/not_authorized/",
            "Method": "GET",
            "Description": "Not authorized",
            "Body": None,
        },
    ]
    return Response(routes)


@api_view(['GET'])
def not_authorized(request):
    return Response({'status': "401 Not Authorized"})
