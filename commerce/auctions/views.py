from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Listing
from .models import User


def index(request):
    lists = Listing.objects.filter(activeListing=True)
    return render(request, "auctions/index.html", {
        "lists": lists,
    })

def listingPage(request, iteamName):
    lst = Listing.objects.filter(iteamName=iteamName).first()
    return render(request, "auctions/listingPage.html",{
        "list": list,
    })

def createListing(request):
    if request.method == "POST":
        iteamName = request.POST.get("iteamName")
        iteamDescription = request.POST.get("iteamDescription")
        minimumBid = request.POST.get("minimumBid")
        iteamImage = request.POST.get("iteamImage")
        activeListing = request.POST.get("activeListing", True) == 'on'
        user = User.objects.get(pk=request.user.id)
        list = Listing(user=user, iteamName=iteamName, iteamDescription=iteamDescription, minimumBid=minimumBid, iteamImage=iteamImage, activeListing=activeListing, maximumBid=minimumBid)
        list.save()
    return render(request, "auctions/createListing.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
