from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.pk}: {self.username}"

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    iteamName = models.CharField(max_length=64)
    iteamDescription = models.CharField(max_length=300)
    minimumBid = models.PositiveBigIntegerField()
    iteamImage = models.CharField(max_length=300)
    activeListing = models.BooleanField(default=True)
    maximumBid = models.PositiveBigIntegerField()

    def __str__(self):
        return f"{self.iteamName}"
