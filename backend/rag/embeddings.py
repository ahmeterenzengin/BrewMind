"""
Embedding service using sentence-transformers.
Model: all-MiniLM-L6-v2 (384 dimensions)
"""
from sentence_transformers import SentenceTransformer

_model = None


def get_model() -> SentenceTransformer:
    """Lazy-load the embedding model (singleton)."""
    global _model
    if _model is None:
        print("[Embeddings] Loading sentence-transformers model...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        print("[Embeddings] Model loaded.")
    return _model


def get_embedding(text: str) -> list[float]:
    """Convert a text string to a 384-dim embedding vector."""
    model = get_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def get_coffee_text(coffee) -> str:
    """Build a rich text representation of a coffee for embedding."""
    ingredients = ", ".join(coffee.ingredients) if coffee.ingredients else ""
    return (
        f"{coffee.name}. {coffee.description}. "
        f"Category: {coffee.get_category_display()}. "
        f"Milk: {coffee.get_milk_type_display()}. "
        f"Sweetness: {coffee.get_sweetness_display()}. "
        f"Intensity: {coffee.get_intensity_display()}. "
        f"Ingredients: {ingredients}."
    )
