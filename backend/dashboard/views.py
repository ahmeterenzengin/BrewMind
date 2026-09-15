from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Avg
from django.db.models.functions import TruncDay, TruncWeek
from django.utils import timezone
from datetime import timedelta

from coffees.models import Coffee, SearchLog, CoffeeOrder
from coffees.serializers import SearchLogSerializer


class TopCoffeesView(APIView):
    """GET /api/dashboard/top-coffees/ - Most ordered coffees"""

    def get(self, request):
        top = (
            CoffeeOrder.objects
            .values("coffee__id", "coffee__name", "coffee__category", "coffee__image_url")
            .annotate(order_count=Count("id"))
            .order_by("-order_count")[:10]
        )
        return Response(list(top))


class CategoryDistributionView(APIView):
    """GET /api/dashboard/category-distribution/ - Orders by category"""

    def get(self, request):
        dist = (
            CoffeeOrder.objects
            .values("coffee__category")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        return Response(list(dist))


class TrendsView(APIView):
    """GET /api/dashboard/trends/?period=daily|weekly"""

    def get(self, request):
        period = request.query_params.get("period", "daily")
        since = timezone.now() - timedelta(days=30 if period == "daily" else 84)

        if period == "weekly":
            qs = (
                SearchLog.objects
                .filter(created_at__gte=since)
                .annotate(period=TruncWeek("created_at"))
                .values("period")
                .annotate(count=Count("id"))
                .order_by("period")
            )
        else:
            qs = (
                SearchLog.objects
                .filter(created_at__gte=since)
                .annotate(period=TruncDay("created_at"))
                .values("period")
                .annotate(count=Count("id"))
                .order_by("period")
            )

        return Response(list(qs))


class RecentSearchesView(APIView):
    """GET /api/dashboard/recent-searches/ - Last 20 searches"""

    def get(self, request):
        logs = SearchLog.objects.select_related("recommended_coffee")[:20]
        serializer = SearchLogSerializer(logs, many=True)
        return Response(serializer.data)


class StatsView(APIView):
    """GET /api/dashboard/stats/ - General KPI stats"""

    def get(self, request):
        total_searches = SearchLog.objects.count()
        total_orders = CoffeeOrder.objects.count()
        unique_coffees_ordered = CoffeeOrder.objects.values("coffee").distinct().count()
        avg_similarity = SearchLog.objects.aggregate(avg=Avg("similarity_score"))["avg"] or 0

        return Response({
            "total_searches": total_searches,
            "total_orders": total_orders,
            "unique_coffees_ordered": unique_coffees_ordered,
            "avg_similarity_score": round(avg_similarity * 100, 1),
        })
