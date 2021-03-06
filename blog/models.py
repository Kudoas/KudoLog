from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from markdownx.models import MarkdownxField

from accounts.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_img = models.ImageField(upload_to='post', blank=True)
    title = models.CharField(max_length=200)
    CATEGORY_CHOICES = (
        ('general', '一般'),
        ('world', '世の中'),
        ('political economy', '政治と経済'),
        ('liviing', '暮らし'),
        ('study', '学び'),
        ('technology', 'テクノロジー'),
        ('interesting', 'おもしろ'),
        ('entertainment', 'エンタメ'),
        ('anime&games', 'アニメとゲーム'),
        ('home appliance', '家電'),
    )
    category = models.CharField(
        max_length=50, blank=True, choices=CATEGORY_CHOICES
    )
    text = MarkdownxField(help_text='Markdownに対応しています')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def late_five_post(self):
        return self.post_set.order_by('published_date').reverse[:4]

    def summary(self):
        return self.text[:50]

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        'blog.Post', related_name='comments', on_delete=models.CASCADE
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('blog/post_list')

    def __str__(self):
        return self.text
