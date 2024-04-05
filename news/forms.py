from django import forms
from django.core.exceptions import ValidationError
from django.views.generic import CreateView

from .models import Post


class PostForm(forms.ModelForm):
    description = forms.CharField(min_length=5)

    class Meta:
        model = Post
        fields = ['titlePost', 'textPost', 'authorPost']

    def clean(self):
        cleaned_data = super().clean()
        textPost = cleaned_data.get("textPost")
        titlePost = cleaned_data.get("titlePost")
        authorPost = cleaned_data.get("authorPost")

        if titlePost == textPost:
            raise ValidationError(
                "Текст не должен быть идентичен названию."
            )
        return cleaned_data


