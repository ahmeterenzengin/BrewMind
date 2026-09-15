import { Link, useLocation } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
  const { pathname } = useLocation();

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <span className="brand-icon">☕</span>
        <span className="brand-name">BrewMind</span>
      </div>
      <div className="navbar-links">
        <Link to="/" className={pathname === "/" ? "nav-link active" : "nav-link"}>
          Discover
        </Link>
        <Link
          to="/dashboard"
          className={pathname === "/dashboard" ? "nav-link active" : "nav-link"}
        >
          Dashboard
        </Link>
      </div>
    </nav>
  );
}
