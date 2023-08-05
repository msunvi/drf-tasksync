from django.db.models import Count

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from .serializer import UserSerializer, TodoItemSerializer, ReviewSerializer
from .models import User, TodoItem, Review


class UserViewSet(ModelViewSet):
    queryset = User.objects.annotate(todo_items=Count('todoitem')).all()
    serializer_class = UserSerializer

    def destroy(self, request, *args, **kwargs):
        if User.objects.filter(todoitem__id=kwargs['pk']).count() > 0:
            return Response({
                'error': 'User cannot be deleted because it has a todo item'
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class TodoItemViewSet(ModelViewSet):
    queryset = TodoItem.objects.select_related('user').all()
    serializer_class = TodoItemSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        return {'todoitem_id': self.kwargs['todos_pk']}

    def get_queryset(self):
        return Review.objects.filter(todoitem_id=self.kwargs['todos_pk'])
