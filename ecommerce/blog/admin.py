from django.contrib import admin

# Register your models here.
from .models import Post, Document
# Register your models here.
admin.site.register(Post)
admin.site.register(Document)