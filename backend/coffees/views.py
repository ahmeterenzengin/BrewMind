from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Coffee, SearchLog, CoffeeOrder
from .serializers import CoffeeSerializer, SearchResponseSerializer
from rag.retriever import search_similar_coffees
from rag.generator import generate_recommendation


class CoffeeListView(APIView):
    """GET /api/coffee/ - List all coffees"""
    authentication_classes = []

    def get(self, request):
        coffees = Coffee.objects.all()
        serializer = CoffeeSerializer(coffees, many=True)
        return Response(serializer.data)


class CoffeeDetailView(APIView):
    """GET /api/coffee/<id>/ - Get single coffee"""
    authentication_classes = []

    def get(self, request, pk):
        coffee = get_object_or_404(Coffee, pk=pk)
        serializer = CoffeeSerializer(coffee)
        return Response(serializer.data)


class CoffeeSearchView(APIView):
    """POST /api/coffee/search/ - RAG based semantic search"""
    authentication_classes = []

    def post(self, request):
        query = request.data.get("query", "").strip()
        if not query:
            return Response(
                {"error": "Query is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 1. Embed query (lazy import so startup is instant)
        from rag.embeddings import get_embedding
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
    """POST /api/coffee/<id>/select/ - Record a coffee selection/order"""
    authentication_classes = []

    def post(self, request, pk):
        coffee = get_object_or_404(Coffee, pk=pk)

        # Siparişi kaydet (CoffeeOrder)
        CoffeeOrder.objects.create(coffee=coffee)

        # Kullanıcı arama yaptıktan sonra butona tıkladığı için,
        # sistemdeki en son yapılan aramayı "Seçildi (Evet)" olarak işaretle.
        latest_log = SearchLog.objects.order_by("-created_at").first()
        if latest_log and latest_log.was_selected == False:
            latest_log.was_selected = True
            latest_log.save()

        return Response({"message": f"Order recorded for {coffee.name}"})
