import { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend,
  LineChart, Line, CartesianGrid,
} from "recharts";
import StatCard from "../components/StatCard";
import {
  getStats, getTopCoffees, getCategoryDistribution,
  getTrends, getRecentSearches,
} from "../services/api";
import "./DashboardPage.css";

const PIE_COLORS = ["#d29b5a", "#5a9bd2", "#5ad28e"];
const BAR_COLOR = "#d29b5a";
const LINE_COLOR = "#f0c070";

function formatPeriod(p) {
  if (!p) return "";
  const d = new Date(p);
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

export default function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [topCoffees, setTopCoffees] = useState([]);
  const [categoryDist, setCategoryDist] = useState([]);
  const [trends, setTrends] = useState([]);
  const [recentSearches, setRecentSearches] = useState([]);
  const [trendPeriod, setTrendPeriod] = useState("daily");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      getStats(),
      getTopCoffees(),
      getCategoryDistribution(),
      getRecentSearches(),
    ]).then(([s, t, c, r]) => {
      setStats(s.data);
      setTopCoffees(t.data);
      setCategoryDist(c.data.map((d) => ({
        name: d.coffee__category.charAt(0).toUpperCase() + d.coffee__category.slice(1),
        value: d.count,
      })));
      setRecentSearches(r.data);
      setLoading(false);
    });
  }, []);

  useEffect(() => {
    getTrends(trendPeriod).then(({ data }) => {
      setTrends(data.map((d) => ({ period: formatPeriod(d.period), count: d.count })));
    });
  }, [trendPeriod]);

  if (loading) {
    return (
      <div className="dashboard-loading">
        <span>📊</span>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <h1 className="dash-title">Dashboard</h1>
      <p className="dash-subtitle">Coffee ordering insights and trends</p>

      {/* KPI Cards */}
      <section className="kpi-grid">
        <StatCard icon="🔍" label="Total Searches" value={stats?.total_searches ?? 0} />
        <StatCard icon="☕" label="Total Orders" value={stats?.total_orders ?? 0} />
        <StatCard icon="🌟" label="Unique Coffees Ordered" value={stats?.unique_coffees_ordered ?? 0} />
        <StatCard
          icon="🎯"
          label="Avg. Similarity Score"
          value={`${stats?.avg_similarity_score ?? 0}%`}
          sub="Vector match quality"
        />
      </section>

      {/* Charts Row */}
      <div className="charts-row">
        {/* Top Coffees Bar Chart */}
        <div className="chart-card">
          <h2 className="chart-title">Top Ordered Coffees</h2>
          {topCoffees.length === 0 ? (
            <p className="chart-empty">No orders yet.</p>
          ) : (
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={topCoffees} layout="vertical" margin={{ left: 10 }}>
                <XAxis type="number" tick={{ fill: "#806050", fontSize: 12 }} />
                <YAxis
                  type="category"
                  dataKey="coffee__name"
                  tick={{ fill: "#a08060", fontSize: 12 }}
                  width={120}
                />
                <Tooltip
                  contentStyle={{ background: "#1a0f08", border: "1px solid #d29b5a30", borderRadius: 8 }}
                  labelStyle={{ color: "#f0c070" }}
                  itemStyle={{ color: "#d29b5a" }}
                />
                <Bar dataKey="order_count" fill={BAR_COLOR} radius={[0, 6, 6, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* Category Pie Chart */}
        <div className="chart-card">
          <h2 className="chart-title">Orders by Category</h2>
          {categoryDist.length === 0 ? (
            <p className="chart-empty">No orders yet.</p>
          ) : (
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie
                  data={categoryDist}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {categoryDist.map((_, i) => (
                    <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                  ))}
                </Pie>
                <Legend
                  wrapperStyle={{ color: "#a08060", fontSize: 13 }}
                />
                <Tooltip
                  contentStyle={{ background: "#1a0f08", border: "1px solid #d29b5a30", borderRadius: 8 }}
                  itemStyle={{ color: "#d29b5a" }}
                />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      {/* Trends Line Chart */}
      <div className="chart-card full-width">
        <div className="chart-title-row">
          <h2 className="chart-title">Search Trends</h2>
          <div className="period-toggle">
            {["daily", "weekly"].map((p) => (
              <button
                key={p}
                className={`period-btn ${trendPeriod === p ? "active" : ""}`}
                onClick={() => setTrendPeriod(p)}
              >
                {p.charAt(0).toUpperCase() + p.slice(1)}
              </button>
            ))}
          </div>
        </div>
        {trends.length === 0 ? (
          <p className="chart-empty">Not enough data yet.</p>
        ) : (
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={trends} margin={{ left: 0, right: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(210,155,90,0.1)" />
              <XAxis dataKey="period" tick={{ fill: "#806050", fontSize: 12 }} />
              <YAxis tick={{ fill: "#806050", fontSize: 12 }} />
              <Tooltip
                contentStyle={{ background: "#1a0f08", border: "1px solid #d29b5a30", borderRadius: 8 }}
                labelStyle={{ color: "#f0c070" }}
                itemStyle={{ color: LINE_COLOR }}
              />
              <Line
                type="monotone"
                dataKey="count"
                stroke={LINE_COLOR}
                strokeWidth={2}
                dot={{ fill: LINE_COLOR, r: 4 }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>

      {/* Recent Searches Table */}
      <div className="chart-card full-width">
        <h2 className="chart-title">Recent Searches</h2>
        {recentSearches.length === 0 ? (
          <p className="chart-empty">No searches yet.</p>
        ) : (
          <div className="table-wrap">
            <table className="searches-table">
              <thead>
                <tr>
                  <th>Query</th>
                  <th>Recommended Coffee</th>
                  <th>Match %</th>
                  <th>Selected</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {recentSearches.map((log) => (
                  <tr key={log.id}>
                    <td className="query-cell">{log.query_text}</td>
                    <td>{log.coffee_name || "-"}</td>
                    <td>{log.similarity_score ? `${Math.round(log.similarity_score * 100)}%` : "-"}</td>
                    <td>
                      <span className={log.was_selected ? "tag yes" : "tag no"}>
                        {log.was_selected ? "Yes" : "No"}
                      </span>
                    </td>
                    <td>{new Date(log.created_at).toLocaleDateString("en-US")}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
