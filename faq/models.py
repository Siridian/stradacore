from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


class Tag(models.Model):
    name = models.CharField(
        "mot",
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "mot-clé"
        verbose_name_plural = "mots-clé"


class Answer(models.Model):
    title = models.CharField(
        "question posée",
        max_length=100,
        unique=True,
        default="Ex: 'Combien font deux et deux ?'"
    )
    upload_content = RichTextUploadingField(
        "réponse apportée",
        default="Ex: 'Deux et deux font quatre'",
        blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="answers",
        blank=True,
        verbose_name="mots-clé"
    )
    user_approval = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "réponse"
        verbose_name_plural = "réponses"


class Question(models.Model):
    content = models.TextField("question utilisateur")
    mail = models.EmailField("mail utilisateur", blank=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "question"
        verbose_name_plural = "questions"


class AnsweredQuestion(models.Model):
    user_question = models.TextField()
    validated_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)