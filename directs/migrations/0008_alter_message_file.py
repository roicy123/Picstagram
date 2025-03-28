# Generated by Django 5.1.4 on 2025-03-17 16:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directs', '0007_message_file_message_message_type_alter_message_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='message_files/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['webm', 'mp3', 'wav', 'ogg', 'jpg', 'jpeg', 'png', 'mp4', 'pdf'])]),
        ),
    ]
