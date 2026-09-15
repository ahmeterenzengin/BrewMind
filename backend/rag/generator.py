"""
LLM generator for coffee recommendations.
Currently: LM Studio (OpenAI-compatible local API)
Future: Claude API (Anthropic)
"""
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.conf import settings


def _build_prompt(query: str, results: list[dict]) -> str:
    """Build the RAG prompt for the LLM."""
    coffee_list = "\n".join(
        f"- {r['coffee'].name}: {r['coffee'].description} "
        f"({r['coffee'].get_category_display()}, {r['coffee'].get_milk_type_display()} milk, "
        f"{r['coffee'].get_intensity_display()} intensity, {r['coffee'].get_sweetness_display()} sweetness)"
        for r in results
    )

    return f"""A customer said: "{query}"

Based on their request, we found these matching coffees:
{coffee_list}

INSTRUCTIONS:
You are a friendly barista assistant. Write a warm, enthusiastic 2-3 sentence recommendation explaining why these coffees match their request.
- Be conversational.
- Mention the top match specifically.
- Keep it concise (maximum 3 sentences).
- Use a coffee emoji.
- DO NOT output any internal thoughts, alternative responses, or notes.
- ONLY output the final response that the customer will see.

Your response:"""


def generate_recommendation(query: str, results: list[dict]) -> str:
    """Generate an LLM recommendation for the given query and coffee results."""
    if not results:
        return "I couldn't find any coffees matching your description. Try describing the flavor, temperature, or milk preference!"

    prompt = _build_prompt(query, results)

    provider = getattr(settings, "LLM_PROVIDER", "LM_STUDIO")

    if provider == "CLAUDE":
        return _generate_claude(prompt)
    elif provider == "GEMINI":
        return _generate_gemini(prompt)
    else:
        return _generate_lm_studio(prompt)


def _generate_lm_studio(prompt: str) -> str:
    """Call LM Studio local OpenAI-compatible API."""
    try:
        from openai import OpenAI

        client = OpenAI(
            base_url=settings.LM_STUDIO_BASE_URL,
            api_key="lm-studio",  # LM Studio does not require a real key
        )

        response = client.chat.completions.create(
            model=settings.LM_STUDIO_MODEL,
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,  # Lower temperature for more focused output
            max_tokens=150,   # Keep it short to prevent run-on thoughts
        )
        content = response.choices[0].message.content
        if content and content.strip():
            return content.strip()

        # Some models return empty content via chat API — try completions endpoint
        comp_response = client.completions.create(
            model=settings.LM_STUDIO_MODEL,
            prompt=f"You are a friendly barista.\n\n{prompt}\n\nRecommendation:",
            temperature=0.7,
            max_tokens=200,
        )
        comp_text = comp_response.choices[0].text
        if comp_text and comp_text.strip():
            return comp_text.strip()

        print("[LM Studio] Model returned empty content, using fallback")
        return _fallback_recommendation(prompt)

    except Exception as e:
        print(f"[LM Studio] Error: {e}")
        return _fallback_recommendation(prompt)


def _generate_claude(prompt: str) -> str:
    """Call Anthropic Claude API."""
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text.strip()
    except Exception as e:
        print(f"[Claude] Error: {e}")
        return _fallback_recommendation(prompt)


def _generate_gemini(prompt: str) -> str:
    """Call Google Gemini API using OpenAI-compatible endpoint."""
    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=settings.GEMINI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )

        response = client.chat.completions.create(
            model=getattr(settings, "GEMINI_MODEL", "models/gemini-3.6-flash"),
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
            max_tokens=1000,
        )
        content = response.choices[0].message.content
        if content and content.strip():
            return content.strip()

        print("[Gemini] Model returned empty content, using fallback")
        return _fallback_recommendation(prompt)

    except Exception as e:
        print(f"[Gemini] Error: {e}")
        return _fallback_recommendation(prompt)


def _fallback_recommendation(prompt: str) -> str:
    """Fallback if LLM is unavailable — simple rule-based response."""
    return (
        "☕ Great choice! Based on your preferences, we found some perfect matches for you. "
        "Each of these coffees has been selected to match your taste profile. Enjoy!"
    )
