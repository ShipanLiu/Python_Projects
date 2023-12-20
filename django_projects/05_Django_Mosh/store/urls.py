

from django.urls import path, include
from . import views
# in views.py we have used viewset, so here we need to apply routers, DefaultRouter as more features "http://localhost:8000/store/products.json" give you all json
# from rest_framework.routers import SimpleRouter, DefaultRouter
# pretty print in python
from pprint import pprint

# 来自 drf-nested-routers
from rest_framework_nested import routers


# initialize the router, create a router instance
router = routers.DefaultRouter()
# register router
# not "products/", but just "products"
# this means: ProductViewSet is responsiable for all products related endpoints.
router.register("products", views.ProductViewSet, basename="products") # based on the "basename" 最终名字可能是 "product-list" or "product_details"
router.register("collections", views.CollectionViewSet, basename="collections")
router.register("carts", views.CartViewSet, basename="carts")
# add endpoints for customer (这里不需要nested router), after add this, then go to "" and you can find a ned endpoint is added
router.register("customers", views.CustomerViewSet, basename="customers")

# start implement nested router

# (parent-router, parent-prefix, lookup="product", this mean we are gonna to have a "product_pk"
products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
carts_router = routers.NestedDefaultRouter(router, "carts", lookup="cart") # "carts" ---自动生成--->  carts_pk
# register child, basename 讲解见上面
products_router.register("reviews", views.ReviewViewSet, basename="product-reviews")
carts_router.register("items", views.CartItemViewSet, basename="carts-items") #the drf will create for us 2 route based on the basename: "carts-items-datail", "carts-items-list"






# pprint(router.urls)
# result ==> you found that all urls are prepared for you
# [<URLPattern '^products/$' [name='product-list']>,
#  <URLPattern '^products/(?P<pk>[^/.]+)/$' [name='product-detail']>,
#  <URLPattern '^collections/$' [name='collection-list']>,
#  <URLPattern '^collections/(?P<pk>[^/.]+)/$' [name='collection-detail']>]

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(products_router.urls)),
    path(r"", include(carts_router.urls)),
]

#URLConf
# urlpatterns = [
#
#     path("", include(router.urls))


    # >>>>down is traditional way not using router>>>>>>>>>>>>>
    # path("products/", views.ProductViewSet.as_view(), name="products_list_url"),
    # # unit the rules ==> write "pk" not "id"
    # path("products/<int:pk>", views.ProductViewSet.as_view(), name="products_detail_url"),
    #
    # path("collections/", views.CollectionList.as_view(), name="collections_list_url"),
    # path("collections/<int:pk>", views.CollectionDetail.as_view(), name="collections_detail_url"),



    #>>>>>>>>>>>>>>down is function based>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # path("hello/", views.say_hallo),
    # path("products/", views.product_list),
    # path("products/<int:id>/", views.product_detail),
    #
    # path("collections/", views.collection_list),

    # hyperlink for collelction
    # the path attribute has to be "pk", not "id"
    # the error if you use "id" but not "pk": "Could not resolve URL for hyperlinked relationship using view name "collection-detail". You may have failed to include the related model in your API, or incorrectly configured the `lookup_field` attribute on this field."
    # path("collections/<int:pk>", views.collection_detail, name="collection-detail")

# ]
