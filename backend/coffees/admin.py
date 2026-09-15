from django.contrib import admin
from .models import Coffee, SearchLog, CoffeeOrder


@admin.register(Coffee)
class CoffeeAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "milk_type", "intensity", "sweetness", "price", "created_at"]
    list_filter = ["category", "milk_type", "intensity", "sweetness"]
    search_fields = ["name", "description"]
    ordering = ["name"]


@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ["query_text", "recommended_coffee", "similarity_score", "was_selected", "created_at"]
    list_filter = ["was_selected"]
    ordering = ["-created_at"]


@admin.register(CoffeeOrder)
class CoffeeOrderAdmin(admin.ModelAdmin):
    list_display = ["coffee", "created_at"]
    ordering = ["-created_at"]
