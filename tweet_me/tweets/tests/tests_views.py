from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from ..models import Message
from ..factories import MessageFactory

# Create your tests here.
# Need to fake login!!!


class RegisterViewTestCase(TestCase):
    def test_200(self):
        client = Client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)   


class LoginViewTestCase(TestCase):
    def test_200(self):
        client = Client()
        response = client.get("/login")
        self.assertEqual(response.status_code, 200)


class LogoutViewTestCase(TestCase):
    def test_302(self):
        client = Client()
        response = client.get("/logout")
        self.assertEqual(response.status_code, 302)


class HomeViewTestCase(TestCase):
    def test_200(self):
        client = Client()
        response = client.get("/home")
        self.assertEqual(response.status_code, 200)


# Does not work
class CreateMessageViewTestCase(TestCase):
    def test_200(self):
        url = reverse("create")
        data = {}
        client = Client() 
        response = client.post(url, data)
        self.assertEqual(response.status_code, 200)


# Does not work
class DetailMessageViewTestCase(TestCase):
    def test_200(self):
        Message = MessageFactory()

        url = reverse("detail", args=(str(Message.id),))
        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, 200)


class UpdateMessageViewTestCase(TestCase):
    def test_200(self):
        Message = MessageFactory()

        url = reverse("update", args=(str(Message.id),))
        client = Client()
        response = client.post(url)
        self.assertEqual(response.status_code, 200)


# Does not work
class DeleteMessageViewTestCase(TestCase):
    def test_200(self):
        Message = MessageFactory()

        url = reverse("delete", args=(str(Message.id),))
        client = Client()
        response = client.post(url)
        self.assertEqual(response.status_code, 200)

        
class ListMessageViewTestCase(TestCase):
    def test_200(self):
        client = Client()
        response = client.get("list")
        self.assertEqual(response.status_code, 200)

