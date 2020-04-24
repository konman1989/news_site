from django.db import models
from django.urls import reverse

from users.models import CustomUser

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=1)
    # use_for_related_fields = True
    # def published(self, **kwargs):
    #     return self.filter(status=1, **kwargs)


class Post(models.Model):
    STATUS_PENDING, STATUS_APPROVED, STATUS_DECLINED = range(3)
    STATUS = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_DECLINED, 'Declined'),
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=STATUS_PENDING)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='posts')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def approve_post(self):
        if self.author.is_staff:
            self.status = self.STATUS_APPROVED
            self.save()

    def get_absolute_url(self):
        self.approve_post()
        return reverse('home')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    author = models.CharField(max_length=32)
    email = models.EmailField()
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Comment by {self.author} to post {self.post.title}"



