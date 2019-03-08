from django.db import models


class Genre(models.Model):
    genre = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.CharField(max_length=200, default=1)

    def __str__(self):
        return self.genre


class Series(models.Model):
    series = models.CharField(max_length=200)
    author = models.CharField(max_length=200, default='Unknown', null=True)
    genre = models.ForeignKey(Genre, default=series, verbose_name="Genre",
                              on_delete=models.SET_DEFAULT)
    summary = models.TextField()

    class Meta:
        # otherwise we get "Seriess" in the admin panel
        verbose_name_plural = "Series"

    def __str__(self):
        return self.series


class Story(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=200, default='Unknown', blank=True, null=True)
    publish_date = models.CharField('year published', max_length=20)
    series = models.ForeignKey(Series, default=title, verbose_name="Series",
                               on_delete=models.SET_DEFAULT)
    slug = models.CharField(max_length=200, default=1)

    class Meta:
        verbose_name_plural = "stories"

    def __str__(self):
        return self.title
