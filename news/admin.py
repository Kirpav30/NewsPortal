from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import *

class PostTranslateAdmin(TranslationAdmin):
    model = Post


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)