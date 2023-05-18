from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your model here...

class CustomUser(AbstractUser):
    is_premium = models.BooleanField(default=False)
