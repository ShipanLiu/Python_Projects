from django.urls import path, include
from .views import (
    product_list_view,
    product_detail_view,
)

app_name = "t04_restfulApi"

urlpatterns = [
    path("products/", product_list_view, name="products"),
    path("products/<int:id>", product_detail_view, name="product_detail")
]






