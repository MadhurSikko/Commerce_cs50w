from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Bids, Comment
from django.db.models import Min, Max


def index(request):

    return render(request, "auctions/index.html", {
        "lists": Listing.objects.filter(status=True),
    })

def bid(request, title):
    lst = Listing.objects.get(title=title)
    maxBid = Bids.objects.filter(listing=lst).aggregate(Max("value"))
    if Comment.objects.filter(listing=lst).exists():    
        userComments = Comment.objects.filter(listing=lst)
    else:
        userComments = None
    try:
        maxBidder = Bids.objects.get(value=int(maxBid['value__max']))
    except:
        maxBidder = "N/A"

    if request.method == "POST":
        if "highest_bid" in request.POST:
            highest_bid = request.POST.get("highest_bid")

            if int(highest_bid) <= lst.highest_bid:
                return render(request, "auctions/bid.html", {
                    "title": title, 
                    "list": lst,
                    "message": True,
                    "maxBidder": maxBidder,
                    "userComment": userComments,
                })
            else:
                lst.highest_bid = int(highest_bid)
                lst.save()
                try:
                    bid = Bids.objects.get(user=User.objects.get(pk=request.user.id))
                    bid.value = int(highest_bid)
                    bid.save()
                except:
                    bid = Bids(user=User.objects.get(pk=request.user.id), listing=lst, value=lst.highest_bid)
                    bid.save()
        elif "close_listing" in request.POST:
            lst.status = False
            lst.save()
            return HttpResponseRedirect(reverse("index"))
        elif "comment" in request.POST:
            comment = request.POST.get("comment")
            co = Comment(user=User.objects.get(pk=request.user.id), listing=lst, description=comment)
            co.save()
            return HttpResponseRedirect(reverse('bid', args=[title]))
        else:
            pass


    return render(request, "auctions/bid.html", {
        "title": title,
        "list": lst,
        "maxBidder": maxBidder,
        "userComment": userComments,
    })

def createListing(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        title = request.POST.get("title")
        description = request.POST.get("description")
        starting_bid = request.POST.get("starting_bid")
        status = request.POST.get("status", True) == 'on'
        image = request.POST.get("image")
        category = request.POST.get("category")
        print("HELLO")
        lst = Listing(user=user, title=title, description=description, starting_bid=starting_bid, status=status, image=image, category=category, highest_bid=starting_bid)
        lst.save()
        return HttpResponseRedirect(reverse("index"))
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
