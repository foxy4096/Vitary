from rest_framework import serializers

from .models import Vit

class VitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vit
        fields = ('id', 'body', 'image', 'video', 'date', 'like_count', 'user', 'likes', 'to_reply_vits', 'plustag')