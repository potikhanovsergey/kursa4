from django.db import models
# Create your models here.
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    message = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.author + ' - ' + self.title


class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True)


    def __str__(self):
        return self.user.username + ' - ' + str(self.date)
