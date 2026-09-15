import { useState } from "react";
import SearchBar from "../components/SearchBar";
import CoffeeCard from "../components/CoffeeCard";
import { searchCoffees } from "../services/api";
import "./HomePage.css";

export default function HomePage() {
  const [results, setResults] = useState([]);
  const [llmResponse, setLlmResponse] = useState("");
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (q) => {
    setLoading(true);
    setError("");
    setQuery(q);
    setHasSearched(true);
    try {
      const { data } = await searchCoffees(q);
      setResults(data.results || []);
      setLlmResponse(data.llm_response || "");
    } catch (e) {
      setError("Could not reach the server. Make sure the backend is running.");
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home-page">
      {/* Hero section */}
      <section className="hero">
        <h1 className="hero-title">
          Find Your <span className="hero-accent">Perfect Brew</span>
        </h1>
        <p className="hero-subtitle">
          Describe how you're feeling, what you're craving, or the weather outside —
          our AI barista will find the perfect coffee for you.
        </p>
        <SearchBar onSearch={handleSearch} loading={loading} />
      </section>

      {/* LLM Response */}
      {llmResponse && !loading && (
        <section className="llm-section">
          <div className="llm-bubble">
            <span className="llm-avatar">🧑‍🍳</span>
            <p className="llm-text">{llmResponse}</p>
          </div>
        </section>
      )}

      {/* Loading state */}
      {loading && (
        <div className="loading-wrap">
          <div className="loading-dots">
            <span /><span /><span />
          </div>
          <p className="loading-text">Brewing recommendations...</p>
        </div>
      )}

      {/* Error state */}
      {error && <div className="error-msg">{error}</div>}

      {/* Results grid */}
      {!loading && results.length > 0 && (
        <section className="results-section">
          <h2 className="results-title">
            Top picks for &ldquo;{query}&rdquo;
          </h2>
          <div className="results-grid">
            {results.map(({ coffee, similarity_score }) => (
              <CoffeeCard
                key={coffee.id}
                coffee={coffee}
                similarityScore={similarity_score}
              />
            ))}
          </div>
        </section>
      )}

      {/* Empty state */}
      {hasSearched && !loading && results.length === 0 && !error && (
        <div className="empty-state">
          <span className="empty-icon">🔍</span>
          <p>No coffees found. Try describing differently!</p>
        </div>
      )}

      {/* Initial state hint */}
      {!hasSearched && (
        <div className="initial-hint">
          <div className="hint-cards">
            {["Hot ☕", "Cold 🧊", "Frappe 🥤"].map((c) => (
              <div key={c} className="hint-card">{c}</div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
