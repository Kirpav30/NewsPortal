from .models import Post
from modeltranslation.translator import register, TranslationOptions


@register(Post)
class PostTranslate(TranslationOptions):
    fields = ('titlePost', 'textPost')