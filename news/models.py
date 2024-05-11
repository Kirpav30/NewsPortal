from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse

news = 'NW'
article = 'AR'
CHOICE_TYPE = [
    (news, 'Новость'),
    (article, 'Статья')
]


class Author(models.Model):
    userAuthor = models.OneToOneField(User, on_delete=models.CASCADE)
    raitingAuthor = models.FloatField(default=0.0)

    def update_rating(self):
        ratingPost = self.post_set.aggregate(postRating=Sum('raitingPost'))
        pRating = 0
        pRating += ratingPost.get('postRating')

        ratingComment = self.userAuthor.comment_set.aggregate(commentRating=Sum('raitingComment'))
        cRating = 0
        cRating += ratingComment.get('commentRating')

        self.raitingAuthor = pRating * 3 + cRating
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    authorPost = models.ForeignKey(Author, on_delete=models.CASCADE)
    dataPost = models.DateTimeField(auto_now_add=True)
    categoryPost = models.ManyToManyField(Category, through='PostCategory')
    titlePost = models.CharField(max_length=64)
    textPost = models.TextField()
    raitingPost = models.FloatField(default=0.0)
    choicePost = models.CharField(max_length=2, choices=CHOICE_TYPE)

    def like(self):
        self.raitingPost += 1
        self.save()

    def dislike(self):
        self.raitingPost -= 1
        self.save()

    def preview(self):
        return self.textPost[0:123] + '...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    postComment = models.ForeignKey(Post, on_delete=models.CASCADE)
    userComment = models.ForeignKey(User, on_delete=models.CASCADE)
    textComment = models.TextField()
    dataComment = models.DateTimeField(auto_now_add=True)
    raitingComment = models.FloatField(default=0.0)

    def like(self):
        self.raitingComment += 1
        self.save()

    def dislike(self):
        self.raitingComment -= 1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    post = models.ForeignKey(
        to='Post',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    name = models.CharField(max_length=255)