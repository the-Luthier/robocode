from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your model here...


class SubscriptionTypes(models.TextChoices):
    FREE = 'FREE', 'Free'
    PREMIUM = 'PREMIUM', 'Premium'
    PRO = 'PRO', 'Pro'


class User(AbstractUser):
    full_name = models.CharField(max_length=100, blank=False)
    is_premium = models.BooleanField(default=False)
    is_pro = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=False)
    e_mail = models.CharField(max_length=100, blank=False)
    adress = models.CharField(max_length=255, blank=False)
    verification_code = models.CharField(max_length=6, blank=False)
    is_verified = models.BooleanField(default=False, blank=False) 
    date_of_birth = models.DateField()
    subscription_type = models.CharField(
        max_length=7,
        choices=SubscriptionTypes.choices,
        default=SubscriptionTypes.FREE,
    )

    REQUIRED_FIELDS = ['phone_number', 'full_name', 'adress', 'verification_code', 'is_verified', 'date_of_birth',]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=False,blank=False)
    is_admin = models.BooleanField(default=False, blank=False)
    is_client = models.BooleanField(default=True, blank=False)
    id = models.AutoField(primary_key=True)    
    full_name = models.CharField(max_length=200, blank=False)
    phone_number = models.CharField(max_length=15, blank=False)
    e_mail = models.CharField(max_length=100, blank=False)
    adress = models.CharField(max_length=255, blank=False)
    verification_code = models.CharField(max_length=6, blank=False)
    is_verified = models.BooleanField(default=False, blank=False) 
    date_of_birth = models.DateField()

    def __str__(self):
            return f'{self.user.username}\'s profile'    
    


class Subscriptions(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.MultipleObjectsReturned('title', 'description', 'created_at', 'user',)
    

class Device(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    device_token = models.CharField(max_length=255, unique=True)


class Notifications(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.MultipleObjectsReturned('title', 'description',)


    