from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Название', max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField('Описание', blank=True, null=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group,
                              blank=True,
                              null=True,
                              on_delete=models.SET_NULL,
                              related_name='groups')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Список постов'
