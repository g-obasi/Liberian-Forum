from django.contrib import admin

# Register your models here.

from accounts.models import User, UserFollow, UserSocialAccount

from .models import Post, Board, Topic, Attachment

admin.site.register(User)
admin.site.register(UserFollow)
admin.site.register(UserSocialAccount)


admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Attachment)





