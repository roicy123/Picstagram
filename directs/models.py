from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('seen', 'Seen'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    body = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sent')  # New field

    def sender_message(from_user, to_user, body):
        sender_message = Message(
            user=from_user,
            sender=from_user,
            recipient=to_user,
            body=body,
            status='sent'
        )
        sender_message.save()

        recipient_message = Message(
            user=to_user,
            sender=from_user,
            recipient=from_user,
            body=body,
            status='sent'
        )
        recipient_message.save()
        return sender_message

    @staticmethod
    def get_message(user):
        users = []
        messages = Message.objects.filter(user=user).values('recipient').annotate(last=models.Max('date')).order_by('-last')
        for message in messages:
            users.append({
                'user': User.objects.get(pk=message['recipient']),
                'last': message['last'],
                'unread': Message.objects.filter(user=user, recipient__pk=message['recipient'], is_read=False).count()
            })
        return users
