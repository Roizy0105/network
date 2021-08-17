from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("self", related_name="followers")
    following = models.ManyToManyField("self", related_name="following")



class Posts(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("User", related_name="likes")

    def serialize(self):
        return {
        "id": self.id,
        "posted_by": self.user_id.username,
        "content": self.content,
        "timestamp": self.created_at.strftime("%b %d %Y, %I:%M %p"),
        "likes": [user.id for user in self.likes.all()]
        }
