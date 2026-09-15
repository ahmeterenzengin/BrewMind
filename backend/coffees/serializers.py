from rest_framework import serializers
from .models import Coffee, SearchLog, CoffeeOrder


class CoffeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coffee
        fields = [
            "id", "name", "description", "category", "milk_type",
            "sweetness", "intensity", "ingredients", "image_url",
            "price", "created_at",
        ]


class CoffeeSearchResultSerializer(serializers.Serializer):
    coffee = CoffeeSerializer()
    similarity_score = serializers.FloatField()


class SearchResponseSerializer(serializers.Serializer):
    results = CoffeeSearchResultSerializer(many=True)
    llm_response = serializers.CharField()
    query = serializers.CharField()


class SearchLogSerializer(serializers.ModelSerializer):
    coffee_name = serializers.CharField(source="recommended_coffee.name", read_only=True)

    class Meta:
        model = SearchLog
        fields = ["id", "query_text", "coffee_name", "similarity_score", "was_selected", "created_at"]


class CoffeeOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoffeeOrder
        fields = ["id", "coffee", "created_at"]
