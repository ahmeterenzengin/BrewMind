from django.urls import path
from . import views

urlpatterns = [
    path("top-coffees/", views.TopCoffeesView.as_view(), name="top-coffees"),
    path("category-distribution/", views.CategoryDistributionView.as_view(), name="category-distribution"),
    path("trends/", views.TrendsView.as_view(), name="trends"),
    path("recent-searches/", views.RecentSearchesView.as_view(), name="recent-searches"),
    path("stats/", views.StatsView.as_view(), name="stats"),
]
