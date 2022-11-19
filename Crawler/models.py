from django.db import models


# Create your models here.

class WebPages(models.Model):
    
    #Will be the title of the webpage
    title = models.CharField(max_length=1000, blank=True, null=True)
    #meta description of the page
    meta_description = models.TextField(blank=True, null=True)
    #Score that the algorithm will generate base upon the page value
    website_score = models.IntegerField(blank=True, default=5)
    #slug field
    url = models.CharField(max_length=1000)
    #keywords
    keywords = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    
class Images(models.Model):
    
    #slug field
    url = models.CharField(unique=True, max_length=5000)
    #Alt text of image
    alt_text = models.CharField(max_length=300)

    def __str__(self) -> str:
        return  self.alt_text
