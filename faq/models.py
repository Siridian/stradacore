"""
faq/models.py contains the Tag, Answer and Question models, and their managers
"""


from ckeditor_uploader.fields import RichTextUploadingField
from nltk.corpus import stopwords
from django.db import models
from collections import Counter


class TagManager(models.Manager):
    # Manager for the tag model, contains the detect_tags method
    def detect_tags(self, iterable):
        """
        Takes an iterable of several strings,
        and returns a list of tags contained in those strings
        """
        detected_tags = []
        for word in iterable:
            if word not in set(stopwords.words('french')):
                for tag in self.all():
                    if tag.name.lower() in word.lower():
                        detected_tags.append(tag)
        return detected_tags


class AnswerManager(models.Manager):
    # Manager for the answer model, contains the find_and_sort method
    def find_and_sort(self, iterable):
        """
        Find all answers matching an iterable of tags,
        and sort them from most to least relevant
        """
        found_list = []
        for tag in iterable:
            found_list.extend(self.filter(tags__name__icontains=tag))

        sorted_found_list = []
        for answer in Counter(found_list).most_common():
            sorted_found_list.append(answer[0])

        return sorted_found_list


class Tag(models.Model):
    # The Tag model is a simple charfield used to categorize the answers
    name = models.CharField(
        "mot",
        max_length=100,
        unique=True
    )
    objects = TagManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "mot-clé"
        verbose_name_plural = "mots-clé"
        indexes = [
            models.Index(fields=['name'], name='name_idx'),
        ]


class Answer(models.Model):
    """
    The Answer model is the core app functionality.
    It contains a title (string) and a content (using ck_editor upload field).
    Each answer is tagged with one or more tag.
    """

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
    objects = AnswerManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "réponse"
        verbose_name_plural = "réponses"


class Question(models.Model):
    """
    The Question model stores question asked by users, and possibly the
    asker's mail
    """
    content = models.TextField("question utilisateur")
    mail = models.EmailField("mail utilisateur", blank=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "question"
        verbose_name_plural = "questions"


class AnsweredQuestion(models.Model):
    """
    The Answered question model stores connection
    between user queries and relevant Answers
    """
    user_question = models.TextField()
    validated_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)