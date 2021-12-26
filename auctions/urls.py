from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.show_listing, name="listing"),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("delete_from_watchlist/<int:listing_id>", views.delete_from_watchlist, name="delete_from_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("categories/", views.categories, name="categories"),
    path("show_category_listings/<int:category_id>", views.show_category_listings, name="category_listings"),
    path("place_bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction"),
]
