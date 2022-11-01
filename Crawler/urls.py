from django.urls import path
from .views import Viper


urlpatterns = [
    path('viper', Viper.as_view())
]
