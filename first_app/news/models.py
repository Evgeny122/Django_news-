from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
import os
from PIL import Image
from io import BytesIO

User = settings.AUTH_USER_MODEL
class Likes(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    like = models.BooleanField(default=False)

class Dnot_likes(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    dnot_like = models.BooleanField(default=False)


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
    likes = models.ManyToManyField(Likes)
    dnot_likes = models.ManyToManyField(Dnot_likes)
    image = models.ImageField(upload_to='news_images/', default='news_images/default_news.jpg')
    image_thumbnail = models.ImageField(
        upload_to="news_images/",
        default = "news_images/news_images_thumb.jpg",
        null=True, 
        blank=True)
    
    def __str__(self):
        return self.article

    def get_likes(self):
        return self.likes.count()
    
    def get_dont_likes(self):
        return self.dnot_likes.count()
    
    def get_image_name(self):
        return self.image.name if self.image and self.image.name != 'news_images/default_news.jpg' else False
    
    def make_thumbnail(self):
        image = Image.open(self.image)
        image.thumbnail((100, 100), Image.ANTIALIAS)
        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()
        thumb_filename = thumb_name.split('/')[0] + '_thumb' + thumb_extension
        
        thumb_extension = thumb_extension.upper()
        FILE_TYPE = thumb_extension[1:]
        if FILE_TYPE == 'JPG':
            FILE_TYPE = 'JPEG'
    
        temp_thumb = BytesIO()
        if thumb_filename == 'news_images_thumb.jpg':
            return
        image.save(temp_thumb, FILE_TYPE)
        temp_thumb.seek(0)
        self.image_thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

    def save(self, *args, **kwargs):
        self.make_thumbnail()
        super(News, self).save(*args, **kwargs)
      


