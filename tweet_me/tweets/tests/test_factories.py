from django.test import TestCase

import factory

from .models import Message


class MessageFactory(TestCase):
    def test_message(self):
        message = MessageFactory

        self.assertIsNotNone(message.text)
        self.assertIsNotNone(created_at.text)
        self.assertIsNotNone(updated_at.text)
        self.assertIsNotNone(creator.text)
