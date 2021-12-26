# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from auctions.models import User, Listing, ListingCategory, Bidding, Comments, Watchlist




class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name']


class ListingCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']


class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'category', 'status', 'bid_price', 'user', 'image_url', 'created_at', 'updated_at']


class BiddingAdmin(admin.ModelAdmin):
    list_display = ['user', 'items', 'price', 'created_at', 'updated_at']


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'created_at', 'updated_at']


class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'listing', 'date_added']



admin.site.register(User, UserAdmin)
admin.site.register(ListingCategory, ListingCategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bidding, BiddingAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Watchlist, WatchlistAdmin)

