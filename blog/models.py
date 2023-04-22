from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=450)  # заголовок поста
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, )
    body = models.TextField()  # Поле нашего поста
    category = models.ManyToManyField("Category", blank=True, related_name="posts")

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={"id": self.id})

    def __str__(self):  # Метод
        return '{}'.format(self.title)


class Category(models.Model):
    title = models.CharField(max_length=40)

    def get_absolute_url(self):
        return reverse('category_detail_url', kwargs={"id": self.id})

    def __str__(self):
        return "{}".format(self.title)


class Profile(models.Model):
    about_me = models.TextField(blank=True)
    image = models.ImageField(upload_to='profile_image', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username
