from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your model here...


class SubscriptionTypes(models.TextChoices):
    FREE = 'FREE', 'Free'
    PREMIUM = 'PREMIUM', 'Premium'
    PRO = 'PRO', 'Pro'


class CustomUser(AbstractUser):
    is_premium = models.BooleanField(default=False)
    is_pro = models.BooleanField(default=False)
    subscription_type = models.CharField(
        max_length=7,
        choices=SubscriptionTypes.choices,
        default=SubscriptionTypes.FREE,
    )



    