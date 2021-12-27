from accounts.models import User
from forum.models import Topic


def counts(request):
    user_count = User.objects.all().count()
    topic_count = Topic.objects.all().count()
    return {'users_count': user_count, 'topics_count': topic_count}