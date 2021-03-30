#import uuid
from django.db import models


class Message(models.Model):
    msg_id = models.CharField(max_length=50)
    sender = models.CharField(default='Email Address', max_length=50)
    receiver = models.CharField(default='Email Address', max_length=50)
    subject = models.CharField(default='Subject', max_length=50)
    email_content = models.TextField()
    #Attachments = models.FileField(upload_to='documents/')
