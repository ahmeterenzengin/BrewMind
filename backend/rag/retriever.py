"""
pgvector retriever: finds the most similar coffees using cosine similarity.
"""
from pgvector.django import CosineDistance
from coffees.models import Coffee


def search_similar_coffees(query_vector: list[float], top_k: int = 5) -> list[dict]:
    """
    Search for the top_k most similar coffees to the query vector.
    Returns a list of dicts with coffee objects and similarity scores.
    """
    results = (
        Coffee.objects
        .exclude(embedding=None)
        .annotate(distance=CosineDistance("embedding", query_vector))
        .order_by("distance")[:top_k]
    )

    return [
        {
            "coffee": coffee,
            "similarity_score": round(1 - float(coffee.distance), 4),
        }
        for coffee in results
    ]
