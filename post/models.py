from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
#Create ID booleanField
#Create Post Status
#Create editable menu
#Create editable comments



class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance, filename):
     #filesbase, extension = filename.split(".")
     #return "%s/%s/%s" %(instance.id, instance.id, filename)
     return "%s/%s" %(instance.id, filename)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, null=True)
    image = models.ImageField(upload_to=upload_location,
            null=True,
            blank=True,
            width_field="width_field",
            height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft =  models.BooleanField(default=False)
    publish = models.DateTimeField(auto_now=False,auto_now_add=False)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post:detail", kwargs={"slug": self.slug})


    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            self.slug = slug
        super(Post, self).save(*args, **kwargs)


class Meta:
    ordering = ["-timestamp", "-update"]
        #"Picture item 1" -> "Picture-item-1"



class Comment(models.Model):
    post = models.ForeignKey('post.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    # def approve(self):
    #     self.approved_comment = True
    #     self.save()

    def __str__(self):
        return self.text
    



# Create your models here.
# class Article(models.Model):
#     class Meta():
#         db_table = 'article'

#     article_title = models.CharField(max_length=200)
#     article_text = models.TextField()
#     article_date = models.DateField()
#     article_likes = models.IntegerField(default=0)
        
#     def __str__(self):
#         return self.article_title

# class Comments(models.Model):
#     class Meta():
#         db_table = 'comments'

#     comments_text = models.TextField(verbose_name="Текст комментария")
#     comments_date = models.DateField(u'date',auto_now=True)
#     comments_article = models.ForeignKey(Article)
#     comments_author = models.ForeignKey(User)