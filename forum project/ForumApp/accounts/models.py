from datetime import datetime

# Create your models here.

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import PIL
# from PIL import Image
# from PIL import Image


# Create your models here.


def profile_img_directory(instance, filename):
    return 'images/profile_pics/{0}/{1}'.format(instance.username, filename)


class User(AbstractUser):

    SEX = (
        ('M', 'male'),
        ('F', 'female')

    )
    email = models.EmailField(('email address'), unique=True)
    profile_pic = models.ImageField(upload_to=profile_img_directory, help_text="Not more than 2MB or less please",
                                    null=True, blank=True)  # don't forget to install pillow
    date_of_birth = models.DateField("your date of birth", null=True)
    # don't forget to add the choices
    gender = models.CharField(choices=SEX, max_length=1, null=True)
    bio = models.TextField(
        max_length=255, help_text="250 words or less ", blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
   
    last_login = models.DateTimeField(default=timezone.now())
    posts_count = models.IntegerField("how many posts", null=True)

    def __str__(self):
        return self.username

    def total_users_count(self):
        return User.objects.all.count()

    # @property
    # def online(self):
    #     """
    #     Check if is online profile
    #     """
    #     if self.last_seen_datetime:
    #         now = timezone.now()
    #         if now > self.last_seen_datetime + timezone.timedelta(
    #                      seconds=settings.USER_ONLINE_TIMEOUT):
    #             return False
    #         else:
    #             return True
    #     else:
    #         return False

class UserFollow(models.Model):
    user_followers = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')

    user_followings = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followings')


class UserSocialAccount(models.Model):
    SOCIAL_ICONS = (
        ('FACEBOOK', 'social_icons\facebook.png'),
        ('WHATSAPP', 'social_icons\whatsapp.png'),
        ('INSTAGRAM', 'social_icons\instagram.png'),
        ('TWITTER', 'social_icons\twitter.png'),)

    icon = models.CharField(max_length=255, blank=True, choices=SOCIAL_ICONS, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="social_accounts")
    name = models.CharField(max_length=255, blank=True,  null=True)
    url = models.URLField(max_length=255, blank=True,  null=True)
