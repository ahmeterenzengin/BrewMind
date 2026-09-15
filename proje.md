# BrewMind - Proje Dokumantasyonu

RAG (Retrieval-Augmented Generation) tabanli akilli kahve oneri web uygulamasi.

---

# BOLUM 1: MIMARI VE TEKNOLOJILER

## Teknoloji Yigini

| Katman | Teknoloji | Aciklama |
|--------|-----------|----------|
| Frontend | React + Vite | SPA, component-based UI |
| Grafikler | Recharts | Dashboard grafikleri |
| Backend | Python + Django + DRF | Web framework, REST API |
| Veritabani | PostgreSQL + pgvector | Vektor veritabani |
| Embedding | sentence-transformers (MiniLM) | Metin -> vektor |
| LLM (Local) | LM Studio (Gemma vb.) | Yerel yapay zeka |
| LLM (Bulut) | Google Gemini API | Bulut yapay zeka |

## API Endpointleri

| Endpoint | Metot | Aciklama |
|----------|-------|----------|
| /api/coffee/ | GET | Tum kahveler |
| /api/coffee/search/ | POST | RAG arama |
| /api/coffee/id/select/ | POST | Siparis kaydet |
| /api/dashboard/stats/ | GET | KPI istatistikleri |
| /api/dashboard/top-coffees/ | GET | En cok siparis edilenler |
| /api/dashboard/trends/ | GET | Trend grafik |
| /api/dashboard/recent-searches/ | GET | Son aramalar |

---

# BOLUM 2: YEREL CALISTIRMA

1. Docker baslat: docker compose up -d
2. LM Studio ac ve model yukle (port 1234)
3. Django baslat: cd backend && venv\Scripts\python manage.py runserver 8000
4. React baslat: cd frontend && npm run dev
5. http://localhost:5173 adresinden ac

---

# BOLUM 3: TAMAMLANAN ISLER

## Asama 0 - Onkosullar
- [x] Docker Desktop kuruldu

## Asama 1 - Temel Altyapi
- [x] Monorepo yapisi (backend/ + frontend/)
- [x] docker-compose.yml (PostgreSQL + pgvector)
- [x] Django projesi + apps (coffees, dashboard)
- [x] Django modelleri (Coffee, SearchLog, CoffeeOrder)
- [x] Migration'lar (VectorExtension dahil)
- [x] Admin paneli (admin / admin123)
- [x] React projesi (Vite) + npm paketleri

## Asama 2 - RAG Pipeline
- [x] Embedding servisi (all-MiniLM-L6-v2)
- [x] pgvector retriever (CosineDistance)
- [x] LM Studio generator (strict prompting)
- [x] 20 kahve seed data + embedding'ler
- [x] 20 AI kahve gorseli

## Asama 3 - API Katmani
- [x] DRF serializer'lar
- [x] RAG arama view
- [x] Dashboard view'lari
- [x] CORS ve CSRF ayarlari

## Asama 4 - Frontend
- [x] Navbar, SearchBar, CoffeeCard, StatCard
- [x] HomePage + DashboardPage
- [x] Dark premium tema

## Asama 5 - Test ve Polish
- [x] RAG arama testi basarili
- [x] Prompt sizintisi giderildi
- [x] CSRF 403 hatasi cozuldu
- [x] Dinamik .env yapisi kuruldu
- [x] .gitignore olusturuldu

---

# BOLUM 4: BULUTA CIKIS PLANI (~45-60 dk)

| Parca | Platform | Maliyet |
|-------|----------|---------|
| Frontend | Vercel | Ucretsiz |
| Backend | Render.com | Ucretsiz |
| Veritabani | Supabase | Ucretsiz |
| Yapay Zeka | Google Gemini API | Ucretsiz |

## Faz 1: Kod Degisiklikleri (~15 dk)
- generator.py: Gemini API entegrasyonu
- settings.py: DATABASE_URL + whitenoise + dinamik ayarlar
- build.sh: Render deploy scripti

## Faz 2: Hesap Acma (~15-20 dk)
- Gemini API Key: aistudio.google.com
- Supabase: supabase.com (pgvector destekli PostgreSQL)
- Render.com: render.com (Django hosting)
- Vercel: Mevcut hesap

## Faz 3: Deploy (~15-25 dk)
- Supabase'e veri yukleme (migrate + seed)
- Render'a backend deploy
- Vercel'e frontend deploy
- Son test

## Gemini API Ucretsiz Limitleri

| Model | Dakikada (RPM) | Gunde (RPD) |
|-------|:---:|:---:|
| Gemini 3 Flash | ~10 | ~1,500 |
| Gemini 2.5 Flash | ~10 | ~1,500 |
