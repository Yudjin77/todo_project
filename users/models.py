from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    photo = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True, verbose_name='Photo')
    date_birth = models.DateField(null=True, blank=True, verbose_name='Date of Birth')
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name='Slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)