from django.urls import path
from .views import *

urlpatterns = [
    path("", UserCreateList.as_view(), name="user-list-create"),
    path("<int:pk>/", UserUpdateDelete.as_view(), name="user-detail"),
]