from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Message(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('seen', 'Seen'),
    ]

    MESSAGE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('voice', 'Voice'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('file', 'File')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    body = models.TextField(null=True, blank=True)
    file = models.FileField(
        upload_to='message_files/', 
        null=True, 
        blank=True, 
        validators=[
            FileExtensionValidator(
                allowed_extensions=['webm', 'mp3', 'wav', 'ogg', 'jpg', 'jpeg', 'png', 'mp4', 'pdf']
            )
        ]
    )
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sent')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default='text')

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"

    @staticmethod
    def sender_message(from_user, to_user, body, file=None, message_type='text'):
        sender_message = Message(
            user=from_user,
            sender=from_user,
            recipient=to_user,
            body=body,
            file=file,
            message_type=message_type,
            status='sent'
        )
        sender_message.save()

        recipient_message = Message(
            user=to_user,
            sender=from_user,
            recipient=to_user,
            body=body,
            file=file,
            message_type=message_type,
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