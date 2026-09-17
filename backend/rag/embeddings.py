"""
Embedding service using fastembed (ONNX Runtime).
Ultra-lightweight (~35MB RAM), avoids Render 512MB RAM OOM crashes.
Model: sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
"""
_model = None


def get_model():
    """Lazy-load the fastembed model (singleton)."""
    global _model
    if _model is None:
        from fastembed import TextEmbedding

        print("[Embeddings] Loading FastEmbed ONNX model...")
        _model = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
        print("[Embeddings] FastEmbed model loaded.")
    return _model


def get_embedding(text: str) -> list[float]:
    """Convert a text string to a 384-dim embedding vector."""
    model = get_model()
    embeddings = list(model.embed([text]))
    return embeddings[0].tolist()


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
