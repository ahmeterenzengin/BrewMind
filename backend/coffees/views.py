from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Coffee, SearchLog, CoffeeOrder
from .serializers import CoffeeSerializer, SearchResponseSerializer
from rag.embeddings import get_embedding
from rag.retriever import search_similar_coffees
from rag.generator import generate_recommendation


class CoffeeListView(APIView):
    """GET /api/coffee/ - List all coffees"""

    def get(self, request):
        coffees = Coffee.objects.all()
        serializer = CoffeeSerializer(coffees, many=True)
        return Response(serializer.data)


class CoffeeDetailView(APIView):
    """GET /api/coffee/<id>/ - Get a single coffee"""

    def get(self, request, pk):
        coffee = get_object_or_404(Coffee, pk=pk)
        serializer = CoffeeSerializer(coffee)
        return Response(serializer.data)


class CoffeeSearchView(APIView):
    """POST /api/coffee/search/ - RAG-powered coffee search"""

    def post(self, request):
        query = request.data.get("query", "").strip()
        if not query:
            return Response(
                {"error": "Query is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 1. Embed query
        query_vector = get_embedding(query)

        # 2. Retrieve similar coffees
        results = search_similar_coffees(query_vector, top_k=5)

        # 3. Generate LLM response
        llm_response = generate_recommendation(query, results)

        # 4. Log the search (log top result)
        if results:
            top = results[0]
            SearchLog.objects.create(
                query_text=query,
                recommended_coffee=top["coffee"],
                similarity_score=top["similarity_score"],
                llm_response=llm_response,
            )

        # 5. Serialize and return
        response_data = {
            "query": query,
            "results": results,
            "llm_response": llm_response,
        }
        serializer = SearchResponseSerializer(response_data)
        return Response(serializer.data)


class CoffeeSelectView(APIView):
    """POST /api/coffee/<id>/select/ - User selected this coffee"""

    def post(self, request, pk):
        coffee = get_object_or_404(Coffee, pk=pk)

        # Create order record
        CoffeeOrder.objects.create(coffee=coffee)

        # Update the most recent search log for this coffee
        SearchLog.objects.filter(
            recommended_coffee=coffee,
            was_selected=False,
        ).order_by("-created_at").first()
        SearchLog.objects.filter(
            recommended_coffee=coffee,
            was_selected=False,
        ).order_by("-created_at").update(was_selected=True)

        return Response({"message": f"Order recorded for {coffee.name}"})
