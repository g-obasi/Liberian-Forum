import os
import django
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# path = os.path.join(BASE_DIR, 'LibForum.settings')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'path')
# django.setup()
from django.db import transaction
from django.core.management.base import BaseCommand
import random
import os
from forum.models import Attachment, Topic, Post, Board
from accounts.models import User, UserFollow, UserSocialAccount

from forum.factories import UserFactory, UserSocialAccountFactory, TopicFactory, PostFactory, AttachmentFactory, BoardFactory, UserFollowFactory


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        Attachment.objects.all().delete()
        Post.objects.all().delete()
        Topic.objects.all().delete()
        Board.objects.all().delete()
        
        UserFollow.objects.all().delete()
        UserSocialAccount.objects.all().delete()
        User.objects.all().delete()


        self.stdout.write("Creating new data...")
        people = []
        topic_list = []
        board_list = []
        post_list = []

        # USER
        for _ in range(500):
            person = UserFactory()
            people.append(person)
            # user_followers = random.choices(people, k=8)
            # person.followers.add(person)
            # person.followings.add(person)


        for _ in range(500):
            user_followers = random.choice(people)
            UserFollowFactory(user_followers=user_followers, user_followings=user_followers)
            

        # USER SOCIAL ACCOUNTS
        for _ in range(500):
            creator = random.choice(people)
            UserSocialAccountFactory(user=creator)

        # BOARD
        for _ in range(80):
           board_followers = random.choices(people, k=8)
           board = BoardFactory(followers=board_followers)
           board_list.append(board)
           board.followers.add(*board_followers)

        # TOPIC
        for _ in range(50):
            board = random.choice(board_list)
            for _ in range(100):
                created_by = random.choice(people)
                topic = TopicFactory(created_by=created_by, board=board)
                topic_list.append(topic)
                topic_followers = random.choices(people, k=8)
                topic.followers.add(*topic_followers)
      
        # POST
        for _ in range(7500):
            topic = random.choice(topic_list)
            created_by = random.choice(people)
            post = PostFactory(created_by=created_by, topic=topic)
            post_list.append(post)


        # ATTACHMENT
        for _ in range(5000):
            post = random.choice(post_list)
            AttachmentFactory(post=post)

