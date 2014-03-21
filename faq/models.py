from django.db import models


class Topic(models.Model):

    """Generic Topics for FAQ question grouping."""

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField()
    slug = models.SlugField(max_length=150)
    answer = models.TextField()
    topic = models.ForeignKey(Topic)
    active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'text']

    def __str__(self):
        return self.text
