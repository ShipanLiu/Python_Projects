from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import ReviewForm

# Create your views here.

class RentalReviewView(TemplateView):
    template_name = 't02_form/rental_review.html'
    form_class = ReviewForm



class ThankYouView(TemplateView):
    template_name = 't02_form/thank_you.html'
