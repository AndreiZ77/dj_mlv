from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time

def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True) # db_index для быстрого поиска
    slug = models.SlugField(max_length=150, blank=True, unique=True) # unique автоматом индексируются
    body = models.TextField(blank=True, db_index=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts') # явно указываем свойство для Tag: related_name='posts'
    date_pub = models.DateTimeField(auto_now_add=True) # авто сохранение при записи в БД
    # auto_now изменение каждый раз при изменении объекта

    # вместо в index.html: href="{% url 'post_detail_url' slug=post.slug %}"
    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug}) #псевдоним функции url

    def get_update_url(self): # чтобы не передавать slug для ф-ии url
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): #переопределяем save, чтобы генерить слаг при создании элемента
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title # возвратит заголовок конкретного экземпляра класса Post

    class Meta:
        ordering = ['-date_pub'] #обратный порядок сортировки по дате


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})  # псевдоним функции url

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title'] #порядок сортировки по алфавиту

