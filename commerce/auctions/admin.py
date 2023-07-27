from django.contrib import admin
from .models import Listing, User, Bids, Comment

# Register your models here.
admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Bids)
admin.site.register(Comment)