from django.urls import path
from .crawler import Viper


urlpatterns = [
    path('/crawler', Viper.as_view())
]
