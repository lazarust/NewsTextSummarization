from django.db import models


# Class to handle each site
class Site(models.Model):
    name = models.TextField(null=False, blank=True)
    slug = models.SlugField(null=False, blank=True)
    url_feed = models.TextField(null=False, blank=True)

    class Meta(object):
        verbose_name = "Site"
        verbose_name_plural = "Sites"


# Class to handle each article
class Article(models.Model):
    date = models.DateField()
    site = models.ForeignKey(Site, blank=True, null=True, on_delete=models.SET_NULL)
    summary = models.TextField()
    article_link = models.TextField()
    headline = models.TextField()

    class Meta(object):
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.headline + " " + str(self.date)