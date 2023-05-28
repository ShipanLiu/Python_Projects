from django.urls import path
from . import views


urlpatterns = [
    #匹配的是 http://localhost:8000/music/index,  这里只需要管 index 部分就行。
    path("index", views.index_view)

]
