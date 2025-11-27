# messaging/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

class MessagingSignalTest(TestCase):
    def test_notification_created(self):
        User = get_user_model()
        sender = User.objects.create(username="sender")
        receiver = User.objects.create(username="receiver")

        msg = Message.objects.create(
            sender=sender,
            receiver=receiver,
            content="Hello!"
        )

        self.assertEqual(Notification.objects.count(), 1)
        notif = Notification.objects.first()
        self.assertEqual(notif.user, receiver)
        self.assertEqual(notif.message, msg)

