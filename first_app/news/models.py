from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Commentaries(models.Model):
    class Meta:
        ordering = ['-date']
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False, null=True)

class News(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    article = models.CharField(max_length=100)
    body = models.TextField(blank=True, null=True)
    commentary = models.ManyToManyField(Commentaries)
    
    def __str__(self):
        return self.article
    

