import axios from "axios";

// Dinamik API Adresi: 
// Local'de (bilgisayarda) VITE_API_URL boş olduğu için proxy ("/api") kullanır.
// Vercel'de ise .env dosyasından bulut sunucunuzun adresini çeker.
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/api",
  headers: { "Content-Type": "application/json" },
});

// Coffee endpoints
export const searchCoffees = (query) =>
  api.post("/coffee/search/", { query });

export const getAllCoffees = () =>
  api.get("/coffee/");

export const getCoffee = (id) =>
  api.get(`/coffee/${id}/`);

export const selectCoffee = (id) =>
  api.post(`/coffee/${id}/select/`);

// Dashboard endpoints
export const getTopCoffees = () =>
  api.get("/dashboard/top-coffees/");

export const getCategoryDistribution = () =>
  api.get("/dashboard/category-distribution/");

export const getTrends = (period = "daily") =>
  api.get(`/dashboard/trends/?period=${period}`);

export const getRecentSearches = () =>
  api.get("/dashboard/recent-searches/");

export const getStats = () =>
  api.get("/dashboard/stats/");
