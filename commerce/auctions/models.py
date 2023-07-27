from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "user")
    title = models.CharField(max_length=64)
    description = models.TextField(default=title)
    starting_bid = models.PositiveBigIntegerField()
    status = models.BooleanField(default=True)
    image = models.CharField(max_length=512, blank = True, default="") 
    category = models.CharField(max_length=32,blank=True, default="")
    watchlist = models.ManyToManyField(User,blank=True)
    highest_bid = models.PositiveBigIntegerField()

    def __str__(self):
        return f"{self.user}: {self.title}"

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    value = models.PositiveBigIntegerField()
    
    def __str__(self):
        return f"{self.user}"
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)  
    description = models.TextField(default="")

    def __str__(self):
        return f"{self.user}: {self.listing}"
    
    