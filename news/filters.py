import django_filters
from django.forms import DateInput
from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'titlePost': ['exact'],
            'choicePost': ['exact'],
        }

    dataPost = django_filters.DateFilter(
        field_name='dataPost',
        lookup_expr='gt',
        label='Date',
        widget=DateInput(
            attrs={'type': 'date'},
        ),
    )
