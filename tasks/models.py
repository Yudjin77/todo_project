from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify


class Status(models.TextChoices):
    NEW = 'new', 'New'
    IN_PROGRESS = 'in_progress', 'In progress'
    DONE = 'done', 'Done'

class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Category")
    description = models.TextField(verbose_name='Description')
    publish_status = models.BooleanField(default=False)
    current_status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='user')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Task.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class TaskVote(models.Model):
    LIKES = 1
    DISLIKES = -1
    VOTES_CHOICES = [
        (LIKES, 'Likes'),
        (DISLIKES, 'Dislikes'),
        ]
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote = models.IntegerField(choices=VOTES_CHOICES)

    class Meta:
        unique_together = ('task', 'user')


