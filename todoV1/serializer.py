from rest_framework import serializers

from .models import User, TodoItem, Review


class UserSerializer(serializers.ModelSerializer):
    todo_items = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ["id", "username", 'email', 'todo_items']


class TodoItemSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TodoItem
        fields = ['id', 'title', 'description', 'user']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        todo_id = self.context['todoitem_id']
        return Review.objects.create(todoitem_id=todo_id, **validated_data)