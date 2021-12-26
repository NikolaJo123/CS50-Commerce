from django import forms
from django.forms import ModelForm, TextInput, Textarea
from django.db import models

from .models import Listing, Comments, Bidding


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'description', 'image_url', 'category', 'bid_price')
        labels = {'title': 'title', 'description': 'description', 'bid_price': 'price'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-4', 'placeholder': 'title'}),
            'description': forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-4', 'placeholder': 'description'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control col-md-8 col-lg-4'}),
            'category': forms.Select(attrs={'class': 'form-control col-md-8 col-lg-2'}),
            'bid_price': forms.NumberInput(attrs={'class': 'form-control col-md-8 col-lg-2'}),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ["comment"]
        labels = {'comment': 'comment'}
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-4', 'placeholder': 'Write a comment.'})
        }


class BiddingForm(ModelForm):
    class Meta:
        model = Bidding
        fields = ["price"]
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control col-md-8 col-lg-4'}),
        }
