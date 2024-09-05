from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    
    sender = models.ForeignKey(User,on_delete=models.PROTECT, related_name='fromPerson')
    receiver = models.ForeignKey(User,on_delete=models.PROTECT, related_name='toPerson')
    messge  = models.TextField()
    sentAt = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.messge
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="messenger")
    course = models.CharField(max_length=100,null=True)
    content = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username+"-"+self.content