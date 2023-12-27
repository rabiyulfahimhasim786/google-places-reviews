from django.db import models

# Create your models here.

class Reviews(models.Model):
    website = models.CharField(max_length=255, null=True, blank=True)
    authorname = models.CharField(max_length=255, null=True, blank=True)
    rating = models.TextField(null=True, blank=True)
    relativetimedescription = models.TextField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    date = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s %f" % (self.website, self.date)
