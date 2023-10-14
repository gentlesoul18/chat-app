from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=100, unique= True)
    phone_number = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.username

    def profile(self):
        profile = Profile.objects.get(user=self)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255, blank = True, default= "What a day!")
    avatar = models.ImageField(upload_to="user_avatar", blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user
    

def create_user_profile(created, instance, **kwargs):
    if created:
        Profile.objects.create(user = instance)

def save_user_profile(instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")

    message = models.TextField()
    is_read = models.BooleanField(default=False)

    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['date']
        verbose_name_plural = "Message"

    def __str__(self) -> str:
        return f"{self.sender} - {self.receiver}"
    
    @property
    def sender_profile(self):
        sender_profile = Profile.objects.get(user = self.sender)
        return sender_profile

    @property
    def receiver_profile(self):
        receiver_profile = Profile.objects.get(user = self.receiver)
        return receiver_profile
    