"""

>>>>>explain ‘basename="product-reviews"’
With basename='product-reviews': By specifying this basename, the URL names for the viewset's actions will be prefixed with 'domain-nameservers'.
For example:
The URL name for the list action will be product-reviews-list.
The URL name for the detail action will be product-reviews-detail.

from django.urls import reverse
# Reverse matching a list action
url = reverse('domain-nameservers-list')  就是给 url 起一个名字， basename is used to generate our url patterns


supported urls;

>>products

http://127.0.0.1:8000/store/products
http://127.0.0.1:8000/store/products/1
http://127.0.0.1:8000/store/products/1/reviews/
http://127.0.0.1:8000/store/products/1/reviews/1

>>collections
http://127.0.0.1:8000/store/collections
http://127.0.0.1:8000/store/collections/1

>>products filtering
http://127.0.0.1:8000/store/products?collection_id=1
>>search&filtering(use django_filters)
http://127.0.0.1:8000/store/products/?collection_id=4&unit_price__lt=100&unit_price__gt=90
>>ordering
http://127.0.0.1:8000/store/products/?search=Coffee&ordering=-unit_price&last_update


>>user(create/update)
"http://127.0.0.1:8001/auth/users/"

>>customer(create / update)
"http://127.0.0.1:8001/store/customers/"

>>authentication(jwt):
http://127.0.0.1:8000/auth/jwt/create

>> after successfully logined in, you want to retrieve the profile(in the header add the JWT header, 注意JWT 之后又一个空格)
http://127.0.0.1:8000/auth/users/me/    with header {"Authorization": "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAzMTU2MjQwLCJpYXQiOjE3MDMwNjk4NDAsImp0aSI6IjNkMzBiZmI1YTE5ZDRmNWQ4NzhhNGE1Y2UwYzVmMWQxIiwidXNlcl9pZCI6MX0.VyVLGg_jriYRdHw6y3q7c-L-Bh7p_aqUOOnhRgukThY"}





"""


"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('playground/', include('playground.urls')),
    path('store/', include('store.urls')),
    # use the external library for login in and token
    # this is for creating/updating users : "http://127.0.0.1:8001/auth/users/"
    # 要区分 creating/updating customers: "http://127.0.0.1:8001/store/customers/"
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('__debug__/', include(debug_toolbar.urls)),
]

"""
访问：http://127.0.0.1:8000/auth/

path('auth/', include('djoser.urls')),
path('auth/', include('djoser.urls.jwt')),


/users/

/users/me/

/users/confirm/

/users/resend_activation/

/users/set_password/

/users/reset_password/

/users/reset_password_confirm/

/users/set_username/

/users/reset_username/

/users/reset_username_confirm/

/token/login/ (Token Based Authentication)

/token/logout/ (Token Based Authentication)

/jwt/create/ (JSON Web Token Authentication)

/jwt/refresh/ (JSON Web Token Authentication)

/jwt/verify/ (JSON Web Token Authentication)


"""
