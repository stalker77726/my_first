from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User



class Post(models.Model): #определение нашей модели, post является моделью Django
    author = models.ForeignKey('auth.User')#ссылка на другую модель
    title = models.CharField(max_length=200)#текстовое поле с ограниченым числом символо
    text = models.TextField()#текстовое поле без ограничения длины символов
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)#дата и время

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title#возвращаем текст с заголовком запис

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    def __str__(self):
        return self.user.username