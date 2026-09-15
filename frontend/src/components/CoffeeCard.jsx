import { useState } from "react";
import { selectCoffee } from "../services/api";
import "./CoffeeCard.css";

const CATEGORY_LABELS = { hot: "Hot ☕", cold: "Cold 🧊", frappe: "Frappe 🥤" };
const INTENSITY_COLORS = { light: "#a8d8a8", medium: "#d4a85a", strong: "#c0504d" };

export default function CoffeeCard({ coffee, similarityScore }) {
  const [ordered, setOrdered] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleOrder = async () => {
    if (ordered || loading) return;
    setLoading(true);
    try {
      await selectCoffee(coffee.id);
      setOrdered(true);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const imageSrc = coffee.image_url
    ? `/images/${coffee.image_url}`
    : `/images/placeholder.jpg`;

  return (
    <div className={`coffee-card ${ordered ? "ordered" : ""}`}>
      <div className="card-image-wrap">
        <img
          src={imageSrc}
          alt={coffee.name}
          className="card-image"
          onError={(e) => { e.target.src = "/images/placeholder.jpg"; }}
        />
        {similarityScore !== undefined && (
          <span className="similarity-badge">
            {Math.round(similarityScore * 100)}% match
          </span>
        )}
      </div>

      <div className="card-body">
        <div className="card-header-row">
          <h3 className="card-title">{coffee.name}</h3>
          <span className="card-price">₺{parseFloat(coffee.price).toFixed(0)}</span>
        </div>

        <p className="card-description">{coffee.description}</p>

        <div className="card-badges">
          <span className="badge category">{CATEGORY_LABELS[coffee.category] || coffee.category}</span>
          {coffee.milk_type !== "none" && (
            <span className="badge milk">{coffee.milk_type} milk</span>
          )}
          <span
            className="badge intensity"
            style={{ borderColor: INTENSITY_COLORS[coffee.intensity] }}
          >
            {coffee.intensity}
          </span>
          {coffee.sweetness !== "none" && (
            <span className="badge sweetness">{coffee.sweetness} sweet</span>
          )}
        </div>

        <button
          className={`order-btn ${ordered ? "ordered" : ""}`}
          onClick={handleOrder}
          disabled={ordered || loading}
        >
          {loading ? "Adding..." : ordered ? "✓ Added!" : "I want this!"}
        </button>
      </div>
    </div>
  );
}
