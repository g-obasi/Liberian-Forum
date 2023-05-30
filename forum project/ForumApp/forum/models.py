from datetime import datetime
from uuid import uuid4
from io import BytesIO, StringIO
import sys
from django.db import models
from django.utils.html import mark_safe
from django.shortcuts import reverse
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.auth.models import Permission
from taggit.managers import TaggableManager
# from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
from PIL import Image
from django.utils.translation import gettext_lazy as _
from accounts.models import User

from django.http import HttpResponse

# Create your models here.


def post_img_directory(instance, filename):
    return 'images/post_images/{0}/{1}'.format(instance.post.created_by, filename)


def comment_img_directory(instance, filename):
    return 'images/comment_images/{0}/{1}'.format(instance.post.created_by, filename)


def validate_file_size(file):
    file_size = file.size
    
    if file_size > 5242880: #5mb exact
        raise ValidationError('File too large - 5MB Max')


def validate_image(value):
    ext = os.path.splitext(value.name)[1]
    accepted_ext = ['.png', '.jpg', '.jpeg', '.gif', '.webp']
    if ext not in accepted_ext:
        raise ValidationError('This field accepts only Files in .PNG, .JPG, .JPEG, .GIF,  .WebP Format')


class Board(models.Model):
    name = models.CharField(max_length=50, unique=True)
    parent = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=255, unique=True)
    icon = models.ImageField(upload_to='images/board_icons', null=True, blank=True)
    followers = models.ManyToManyField(User, blank=True, verbose_name='Board_Followers', related_name='board_followers')
    moderators = models.ManyToManyField(User, blank=True,  verbose_name=_('Moderators'),  related_name='board_moderators')
    topic_count = models.IntegerField(_('Topic count'), blank=True, default=0)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def add_permissions_topic_moderator(self, moderator):
        permission1 = Permission.objects.get(codename='add_topic')
        permission2 = Permission.objects.get(codename='change_topic')
        permission3 = Permission.objects.get(codename='delete_topic')
        moderator.user_permissions.add(permission1, permission2, permission3)
        moderator.is_staff = True
        moderator.save()

    # Clear permissions to moderator
    def clear_permissions_moderator(self, moderator):
        moderator.user_permissions.clear()

        # Remove permission is_staff
        moderator.is_staff = False
        moderator.save()


class Topic(models.Model):

    slug = models.SlugField(max_length=80, unique=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='topics')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField("How many views", default=0)
    order = models.IntegerField(_('Order'), blank=True, null=True)
    post_count = models.IntegerField(_('Post count'), blank=True, default=0)
    status = models.CharField(_('Status'), max_length=20, default="Open")
    last_updated = models.DateTimeField(auto_now=True)
    followers = models.ManyToManyField(User, blank=True,  verbose_name=_('Topic Followers'),  related_name='thread_followers')
    tags = TaggableManager()
    # vector_column = SearchVectorField(null=True)  # new field

    class Meta:
        verbose_name = "Topic"
        ordering = ('date_created',)
        # indexes = (GinIndex(fields=["vector_column"]),)  # add index

    def get_absolute_url(self):
        return reverse('thread_post_list', kwargs={'slug':self.slug ,'topic_pk': self.pk})
    
    def get_last_ten_posts(self):
        return self.topic_posts.order_by('-date_created')[:10]

    def num_posts(self):
        return self.post_count

    def num_replies(self):
        return max(0, self.post_set.count() - 1)

    def last_post(self):
        if self.post_set.count():
            return self.post_set.order_by("date_created")[0]


class Post(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=4098, default="Write something here")
    date_created = models.DateTimeField(default=datetime.now)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic_posts')
    liked_by = models.ManyToManyField(User, blank=True, verbose_name=_('Post Liked By'), related_name='post_likes')
    shared_by = models.ManyToManyField(User, blank=True, verbose_name=_('Post Shared By'), related_name='post_shares')
    status = models.BooleanField(_('Status'), default=True)
    user_ip = models.GenericIPAddressField(_('User IP'), blank=True, null=True)
    # vector_column = SearchVectorField(null=True)  # new field

    class Meta:
        # indexes = (GinIndex(fields=['vector_column']),) #index
        ordering = ['date_created']
        verbose_name = _('Post')
            
    def __str__(self):
        return self.topic.title + '/n' + self.message

    def get_absolute_url(self):
        return reverse('thread_post_list', kwargs={'slug':self.topic.slug, 'topic_pk': self.topic.pk})
    
    def get_page_count(self):
        return self.topic.post_count/3


    def totalikescount(self):
        return self.liked_by.count()

    def totalsharescount(self):
        return self.shared_by.count()

    # def get_message_as_markdown(self):
    #     return mark_safe(self.comment_text)


class Attachment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_attachments')
    image = models.ImageField(upload_to=post_img_directory, null=True, blank=True, validators=[validate_image])
    file = models.FileField(upload_to=post_img_directory, null=True, blank=True, validators=[validate_image])
    
    # def handle_images(img):
    #     img = Image.open(img)
    #     if img.mode != 'RGB':
    #         tmp_img = img.convert('RGB')
    #     # if img.name.split('.')[1] =='gif'
    #     output = BytesIO()
    #     tmp_img.save(output, format='JPEG', quality=65)
    #     output.seek(0)
    #     image = InMemoryUploadedFile(output, 'ImageField', '%s.jpg' % img.name.split('.')[0], 'image/jpeg',  sys.getsizeof(output), tmp_img.tell(), None)
    #     return image

    # def save(self, *args, **kwargs):
    #     # img = self.image
    #     # if img:
    #     #     if img.size > 0.3*1024*1024:
    #     #         self.handle_images(img)
    #     super(Attachment, self).save(*args, **kwargs)
