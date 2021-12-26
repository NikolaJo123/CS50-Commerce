from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class ListingCategory(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}: {self.comment}"


class Listing(models.Model):
    STATUS = (
        ("True", "True"),
        ("False", "False"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner", null=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(ListingCategory, on_delete=models.CASCADE)
    image_url = models.URLField()
    status = models.CharField(max_length=10, choices=STATUS, default="True")
    bid_price = models.DecimalField(decimal_places=2, max_digits=10)
    comments = models.ManyToManyField(Comments, blank=True, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Bidding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    price = models.DecimalField(decimal_places=2, max_digits=10)
    items = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="user_bid_items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} placed a bid in for {self.price}."


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listings")
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def price(self):
        return self.listing.bid_price

    @property
    def image(self):
        return self.listing.image_url
