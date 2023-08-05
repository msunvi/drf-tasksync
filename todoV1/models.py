from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class TodoItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(auto_now_add=False, auto_now=False)
    is_complete = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class Review(models.Model):
    todoitem = models.ForeignKey(TodoItem, on_delete=models.CASCADE, related_name='todo')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
