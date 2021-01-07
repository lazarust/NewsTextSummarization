from django.db import models

# Class to handle each site
class Site(models.Model):
    pass


# Class to handle each article
class Article(models.Model):
    date = models.DateField()
    site = models.ManyToManyField(Site, blank=False)
    summary = models.TextField()
    article_link = models.TextField()
    headline = models.TextField()

    class Meta(object):
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.headline + " " + str(self.date)