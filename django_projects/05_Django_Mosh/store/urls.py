from django.urls import path, include
from . import views

#URLConf
urlpatterns = [
    path("hello/", views.say_hallo),
    path("products/", views.product_list),
    path("products/<int:id>/", views.product_detail),

    # hyperlink for collelction
    # the path attribute has to be "pk", not "id"
    # the error if you use "id" but not "pk": "Could not resolve URL for hyperlinked relationship using view name "collection-detail". You may have failed to include the related model in your API, or incorrectly configured the `lookup_field` attribute on this field."
    path("collections/<int:pk>", views.collection_detail, name="collection-detail")

]
