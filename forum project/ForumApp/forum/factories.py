# For creating test data
import factory
import faker
from factory.django import DjangoModelFactory

from .models import Board, Topic, Post, Attachment
from accounts.models import User, UserSocialAccount, UserFollow


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Sequence(lambda n: 'user_name{}'.format(n))
    date_of_birth = factory.Faker("date_of_birth")
    bio = factory.Faker("text")
    location = factory.Faker("address")
    email = factory.Sequence(lambda n: 'user{}@example.com'.format(n))
    gender = factory.Faker("random_element", elements=('F', 'M'))
    password = factory.Faker("md5")
    is_superuser = False

class UserFollowFactory(DjangoModelFactory):
    class Meta:
        model = UserFollow
    
    user_followers = factory.SubFactory(UserFactory)
    user_followings = factory.SubFactory(UserFactory)
    

class UserSocialAccountFactory(DjangoModelFactory):
    class Meta:
        model = UserSocialAccount
    user = factory.SubFactory(UserFactory)
    name = factory.Faker("random_element", elements=('Facebook', 'Twitter', 'WhatsApp', 'Instagram'))
    url = factory.Faker('url')


class BoardFactory(DjangoModelFactory):
    class Meta:
        model = Board

    name = factory.Sequence(lambda n: 'board{}'.format(n))
    description = factory.Faker("sentence", nb_words=5, variable_nb_words=True)
    icon = factory.Faker("file_name")
    topic_count = factory.Faker("random_int")
    
    # for many to many
    @factory.post_generation
    def moderators(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for moderator in extracted:
                self.moderators.add(moderator)

    @factory.post_generation
    def followers(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for follower in extracted:
                self.followers.add(follower)


class TopicFactory(DjangoModelFactory):
    class Meta:
        model = Topic

    slug = factory.Sequence(lambda n: 'topic-slug-post-board{}'.format(n))
    board = factory.SubFactory(BoardFactory)
    created_by = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: ' find a topic post board{}'.format(n))
    date_created = factory.Faker("date")
    featured = factory.Faker("boolean", chance_of_getting_true=20)
    views = factory.Faker("random_int")
    post_count = factory.Faker("random_int")
    # last_updated = factory.Faker("date")
    created_by = factory.SubFactory(UserFactory)
    
    # @factory.post_generation
    # def followers(self, create, extracted, **kwargs):
    #     if not create:
    #         return
    #     if extracted:
    #         for follower in extracted:
    #             self.followers.set(follower)


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    created_by = factory.SubFactory(UserFactory)
    message = factory.Faker("sentence")
    date_created = factory.Faker("date")
    topic = factory.SubFactory(TopicFactory)
    status = factory.Faker("random_element", elements=('True', 'False'))
    user_ip = factory.Faker("ipv4")
    
    @factory.post_generation
    def liked_by(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for user in extracted:
                self.liked_by.add(user)
                
    @factory.post_generation
    def shared_by(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for user in extracted:
                self.shared_by.add(user)


class AttachmentFactory(DjangoModelFactory):
    class Meta:
        model = Attachment

    post = factory.SubFactory(PostFactory)
    # image = factory.Faker("image", size=(700, 840), luminosity= 'bright', image_format='png')
    image = factory.Faker("random_element", elements=(
        'mayra_foto_storia_3.jpg', 'Stripe-fraud_prevention_team.jpg', 'Stripe-IT_department_at_work.jpg',))

