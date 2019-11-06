from django.contrib import admin

from .models import Tag, Answer, Question


admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(Question)