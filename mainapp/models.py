from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
import datetime
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class topicTheme(models.Model):
    name = models.CharField(max_length=255)
    
    
    def __str__(self):
        return self.name

class dkTopic(models.Model):
    topicTheme = models.ForeignKey(topicTheme, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    
class adminPost(models.Model):
    topicTheme = models.ForeignKey(topicTheme, null=True, on_delete=models.SET_NULL)
    dkTopic = models.ForeignKey(dkTopic, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created = models.DateField(('Date'), default=datetime.datetime.now)
    created_at = models.DateTimeField(auto_now_add=True)
    repliers = models.ManyToManyField(User, related_name='repliers', blank=True)
    
    def __str__(self):
        return self.name
    

    
    
class allReply(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    post = models.ForeignKey(adminPost, on_delete=CASCADE, null=False)
    body = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-last_updated', '-created_on']
    
    def __str__( self ):
        return self.body[0:50] 
    

class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    noteTopic = models.ForeignKey(dkTopic, on_delete=models.CASCADE)
    noteTheme = models.ForeignKey(topicTheme, on_delete=models.CASCADE)
    noteContent = models.TextField()
    relatedAdminPost = models.ForeignKey(adminPost, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self ):
        return f"{self.date} - {self.noteTopic} - {self.noteTheme} - {self.relatedAdminPost}"
    
    



class CheckoutSessionRecord(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="The user who initiated the checkout."
    )
    stripe_customer_id = models.CharField(max_length=255)
    stripe_checkout_session_id = models.CharField(max_length=255)
    stripe_price_id = models.CharField(max_length=255)
    has_access = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

