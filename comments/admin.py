from django.contrib import admin
from .models import BannedWord, Comment

admin.site.register(Comment)
# register banned word model to allow superusers to add/edit the words
admin.site.register(BannedWord)
