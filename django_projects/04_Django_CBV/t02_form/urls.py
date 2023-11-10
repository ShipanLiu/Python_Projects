from django.urls import path, include
from t02_form.views import RentalReviewView, ThankYouView

app_name = 't02_form'

urlpatterns = [
    path('rental_review/', RentalReviewView.as_view(), name="rental_review"),
    path('thank_you/', ThankYouView.as_view(), name="thank_you")
]
