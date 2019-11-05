from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Answer(models.Model):
    title = models.CharField(max_length=100, unique=True, default="Ex: 'Combien font deux et deux ?'")
    content = models.TextField(default="Ex: 'Deux et deux font quatre'", blank=True)
    upload_content = RichTextUploadingField(blank=True)
    tags = models.ManyToManyField(Tag, related_name='question', blank=True)
    user_approval = models.IntegerField(default=0)
    primary_key = True

    def __str__(self):
        return self.title


class Question(models.Model):
    content = models.TextField()
    mail = models.EmailField(blank=True)

    def __str__(self):
        return self.content
