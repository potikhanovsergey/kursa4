from django.db import models
from django.utils import timezone, dateformat
from django.conf import settings
# Create your models here.

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
    author_name = models.TextField(max_length=30)
    message = models.CharField(max_length=300)
    date = dateformat.format(timezone.now(), settings.DATE_FORMAT)


    def __str__(self):
        return self.author_name + ' - ' + str(self.date)


