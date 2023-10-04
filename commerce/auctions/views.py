from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing

class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'description', 'starting_bid', 'category', 'image')


def index(request):
    return render(request, "auctions/index.html")


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

    
def create(request):

    # Route reached via POST
    if request.method == "POST":
        
        # Form to create a new listing
        form = NewListingForm(request.POST)

        # Checks if form is valid
        if form.is_valid():

            # Form includes title, description, starting bid, and optional category/image
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            category = form.cleaned_data["category"]
            image = form.cleaned_data["image"]

            # Creates new listing
            listing = Listing.objects.create_listing(title, description, starting_bid, category, image)
            listing.save()

            # Redirect user to the new listing
            return HttpResponseRedirect(reverse("listing", args=(title,)))
        
        # If form is invalid
        else:
            return render(request, "auctions/create.html", {"form": form})
    
    # Route reached via GET
    return render(request, "auctions/create.html", {"form": NewListingForm()})


def listing(request):
    return render(request, "auctions/listing.html")