from django.db import models
from helpers.models import BaseModel
from users.models import User
from taggit.managers import TaggableManager
# Create your models here.


# 게시글 모델
class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    tags = TaggableManager()

    def __str__(self):
        return f'{self.id} - {self.title}'

    def total_likes(self):
        return self.likes.count()


# 댓글 모델
class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f'{self.id} - {self.user}'
