from django.db import models
# Create your models here.
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pages/static/pages/img', max_length=100, default="post-img.png")
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

class Service(models.Model):
    title = models.CharField(max_length=30)
    price = models.CharField(max_length=5)
    description = models.TextField()
    img_title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Client(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=50)



class ClientService(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    is_done = models.BooleanField(default=False)





