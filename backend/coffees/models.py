from django.db import models
from pgvector.django import VectorField


class Coffee(models.Model):
    CATEGORY_CHOICES = [
        ("hot", "Hot"),
        ("cold", "Cold"),
        ("frappe", "Frappe"),
    ]
    MILK_CHOICES = [
        ("none", "None"),
        ("whole", "Whole Milk"),
        ("almond", "Almond Milk"),
        ("oat", "Oat Milk"),
        ("cream", "Cream"),
    ]
    SWEETNESS_CHOICES = [
        ("none", "No Sugar"),
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]
    INTENSITY_CHOICES = [
        ("light", "Light"),
        ("medium", "Medium"),
        ("strong", "Strong"),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    milk_type = models.CharField(max_length=20, choices=MILK_CHOICES, default="none")
    sweetness = models.CharField(max_length=20, choices=SWEETNESS_CHOICES, default="none")
    intensity = models.CharField(max_length=20, choices=INTENSITY_CHOICES, default="medium")
    ingredients = models.JSONField(default=list)
    image_url = models.CharField(max_length=255, blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    embedding = VectorField(dimensions=384, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Coffee"
        verbose_name_plural = "Coffees"

    def __str__(self):
        return self.name


class SearchLog(models.Model):
    query_text = models.TextField()
    recommended_coffee = models.ForeignKey(
        Coffee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="search_logs",
    )
    similarity_score = models.FloatField(default=0.0)
    was_selected = models.BooleanField(default=False)
    llm_response = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Search Log"
        verbose_name_plural = "Search Logs"

    def __str__(self):
        return f"{self.query_text[:50]} -> {self.recommended_coffee}"


class CoffeeOrder(models.Model):
    coffee = models.ForeignKey(
        Coffee,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Coffee Order"
        verbose_name_plural = "Coffee Orders"

    def __str__(self):
        return f"Order: {self.coffee.name} at {self.created_at}"
