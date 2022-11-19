from django.urls import path
from .views import Viper, ViperImage


urlpatterns = [
    path('viper', Viper.as_view()),
    path('viperimage', ViperImage.as_view())
]
