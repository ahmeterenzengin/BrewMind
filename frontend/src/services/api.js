import axios from "axios";

const api = axios.create({
  baseURL: "/api",
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
