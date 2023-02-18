from django.contrib import admin

# Register your models here.
from .models import News, Commentaries

admin.site.register(News)
admin.site.register(Commentaries)