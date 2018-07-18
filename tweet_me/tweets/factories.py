import factory
import factory.fuzzy
from django.contrib.auth.models import User

from .models import Message


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user{}'.format(n))
    password = factory.fuzzy.FuzzyText(10)


# Check to make sure datetime works
class MessageFactory(factory.django.DjangoModelFactory):
    class Meta: 
        model = Message

    text = factory.fuzzy.FuzzyText(length=99)
    # created_at = factory.fuzzy.fdt = FuzzyDateTime(datetime.datetime(2008, 1, 1, tzinfo=UTC)) 
    # updated_at = factory.fuzzy.fdt = FuzzyDateTime(datetime.datetime(2008, 2, 1, tzinfo=UTC)) 
    creator = factory.SubFactory(UserFactory)
