import { useState } from "react";
import "./SearchBar.css";

const SUGGESTIONS = [
  "I want something cold and milky",
  "Strong espresso, no milk",
  "Sweet and chocolatey",
  "Light and refreshing for a hot day",
  "Something cozy and warm",
  "Dairy-free option please",
];

export default function SearchBar({ onSearch, loading }) {
  const [value, setValue] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (value.trim() && !loading) {
      onSearch(value.trim());
    }
  };

  const handleSuggestion = (s) => {
    setValue(s);
    if (!loading) onSearch(s);
  };

  return (
    <div className="searchbar-wrap">
      <form className="searchbar-form" onSubmit={handleSubmit}>
        <div className="searchbar-input-row">
          <span className="searchbar-icon">☕</span>
          <input
            className="searchbar-input"
            type="text"
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder="Describe your perfect coffee… (e.g. icy, milky, sweet)"
            disabled={loading}
          />
          <button className="searchbar-btn" type="submit" disabled={loading || !value.trim()}>
            {loading ? (
              <span className="spin">⟳</span>
            ) : (
              "Find ✨"
            )}
          </button>
        </div>
      </form>

      <div className="suggestion-chips">
        {SUGGESTIONS.map((s) => (
          <button
            key={s}
            className="chip"
            onClick={() => handleSuggestion(s)}
            disabled={loading}
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}
