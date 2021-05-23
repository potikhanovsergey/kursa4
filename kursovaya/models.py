from django.db import models

# Create your models here.

class Post(models.Model):
    author = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=50, null=True)
    message = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.author + ' - ' + self.title
