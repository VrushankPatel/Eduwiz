from django.urls import path, include
from .views import home, features
from .views import home, features
urlpatterns = [
    path('', home),
    path('/features', features)
]
