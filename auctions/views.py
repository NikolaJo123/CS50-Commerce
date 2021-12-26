from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from auctions.forms import ListingForm, CommentForm, BiddingForm
from django.contrib import messages

from .models import User, Listing, Watchlist, ListingCategory


def index(request):
    listings = Listing.objects.filter(status='True')

    context = {
        'listings': listings
    }
    return render(request, "auctions/index.html", context)


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


# >>>>>>>>>>>>>>>>>>>>>> MY FUNCTIONS <<<<<<<<<<<<<<<<<<<


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        user = User.objects.get(username=request.user)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            context = {
                "form": ListingForm()
            }
            return render(request, "auctions/create_listing.html", context)
    else:
        context = {
            "form": ListingForm()
        }
        return render(request, "auctions/create_listing.html", context)


@login_required
def show_listing(request, listing_id):
    user = User.objects.get(username=request.user)
    listing = Listing.objects.get(pk=listing_id)
    form = CommentForm(request.POST, request.FILES)
    bid_form = BiddingForm(request.POST, request.FILES)

    return render(request, "auctions/listing.html", {"listing": listing, 'form': form, 'bid_form': bid_form})


@login_required
def add_to_watchlist(request, listing_id):
    user = User.objects.get(username=request.user)
    listing = Listing.objects.get(pk=listing_id)
    checkinwatchlist = Watchlist.objects.filter(listing_id=listing.id, user_id=user.id)
    last_url = request.META.get('HTTP_REFERER')

    if checkinwatchlist:
        control = 1  # The product is in watchlist
    else:
        control = 0  # The product is not in watchlist

    if request.method == "POST":
        if control == 1:
            messages.info(request, "Product is already in Watchlist! Check the Watchlist menu to view all your favourite lists.")
        else:
            data = Watchlist()
            data.user_id = user.id
            data.listing = listing
            data.save()
            messages.success(request, 'Product added to Watchlist.')

        return HttpResponseRedirect(last_url)
    else:
        context = {
            "listing": listing
        }
        return render(request, "auctions/listing.html", context)


@login_required
def delete_from_watchlist(request, listing_id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = User.objects.get(username=request.user)

    Watchlist.objects.filter(listing=listing_id, user_id=current_user.id).delete()
    messages.warning(request, 'You have deleted an item from your Watchlist!')

    return HttpResponseRedirect(url)


@login_required
def watchlist(request):
    current_user = User.objects.get(username=request.user)
    watchlist = current_user.watchlist.all()
    #listing = Listing.objects.filter(user_id=current_user.id)
    checkinwatchlist = Watchlist.objects.filter(user_id=current_user.id)

    if checkinwatchlist:
        control = True
    else:
        control = False

    context = {
        'watchlist': watchlist,
        'control': control
    }

    return render(request, "auctions/watchlist.html", context)


def comment(request, listing_id):
    user = User.objects.get(username=request.user)
    listing = Listing.objects.get(pk=listing_id)
    last_url = request.META.get('HTTP_REFERER')

    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
            listing.comments.add(data)
            listing.save()

            return HttpResponseRedirect(last_url)
        else:
            context = {
                "form": CommentForm()
            }
            return render(request, "auctions/listing.html", context)
    else:
        context = {
            "form": CommentForm()
        }
        return render(request, "auctions/listing.html", context)


@login_required
def categories(request):
    listing_categories = ListingCategory.objects.filter()
    return render(request, 'auctions/categories.html', { "categories": listing_categories })


@login_required
def show_category_listings(request, category_id):
    cat_listings = ListingCategory.objects.filter()
    listing = Listing.objects.filter(category_id=category_id)
    cat_title = ListingCategory.objects.get(pk=category_id)

    context = {
        "listings": listing,
        "category": cat_listings,
        'title': cat_title
    }
    return render(request, 'auctions/category_listings.html', context)


def place_bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(username=request.user)
    comm_form = CommentForm(request.POST, request.FILES)

    if request.method == "POST":
        price = float(request.POST.get("price"))
        # bids = listing.bids.all()

        if user.username != listing.user.username:
            if price <= listing.bid_price:
                context = {
                    "listing": listing,
                    "bid_form": BiddingForm(),
                    "form": comm_form,
                    "message": "Error! Invalid bid amount! Your amount must be bigger than the initial one!"
                }
                return render(request, "auctions/listing.html", context)

            form = BiddingForm(request.POST, request.FILES)

            if form.is_valid():
                listing.bid_price = price
                listing.save()
            else:
                return render(request, 'auctions/listing.html', {
                    "bid_form": form,
                    "form": comm_form
                })

        context = {
            "listing": listing,
            "bid_form": BiddingForm(),
            "form": comm_form,
            "message": "You successfully made a bidding!!!"
        }
        return render(request, "auctions/listing.html", context)
    else:
        context = {
            "listing": listing,
            "bid_form": BiddingForm(),
            "form": comm_form,
            "message": ""
        }
        return render(request, "auctions/listing.html", context)


def close_auction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(username=request.user)
    last_url = request.META.get('HTTP_REFERER')
    comm_form = CommentForm(request.POST, request.FILES)

    if request.method == "POST":
        messages.warning(request, "You have closed the Auction for this item!")

        listing.status = "False"
        listing.save()

        context = {
            "listing": listing,
            "form": comm_form,
        }
        return render(request, "auctions/listing.html", context)
    else:
        return HttpResponseRedirect(last_url)
