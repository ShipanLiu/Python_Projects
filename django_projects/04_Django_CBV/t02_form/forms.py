from django import forms

class ReviewForm(forms.Form):
    first_name = forms.CharField(label="first_name", max_length=20)
    last_name = forms.CharField(label="last_name", max_length=20)
    email = forms.EmailField()
    review = forms.CharField(label="please input your review here", max_length=500)


