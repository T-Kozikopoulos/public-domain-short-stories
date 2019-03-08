from django.contrib import admin
from .models import Story, Series, Genre
from tinymce.widgets import TinyMCE
from django.db import models


class StoryAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'author',
        'publish_date',
        'slug',
        'series',
        'content'
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }


admin.site.register(Series)
admin.site.register(Genre)
admin.site.register(Story, StoryAdmin)
