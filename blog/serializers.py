from rest_framework import serializers
from .models import BlogData, User


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogData
        fields = ('id', 'author', 'title', 'text', 'published_date', 'upvotes')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')
