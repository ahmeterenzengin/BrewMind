from django.urls import path
from . import views

urlpatterns = [
    path("", views.CoffeeListView.as_view(), name="coffee-list"),
    path("search/", views.CoffeeSearchView.as_view(), name="coffee-search"),
    path("<int:pk>/", views.CoffeeDetailView.as_view(), name="coffee-detail"),
    path("<int:pk>/select/", views.CoffeeSelectView.as_view(), name="coffee-select"),
]
