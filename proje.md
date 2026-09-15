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

# BOLUM 4: BULUTA CIKIS (TEK SERVIS: RENDER + NEON)

Vercel ve Supabase karmasasi kaldirilmistir. Proje tek bir servis olarak Render.com uzerinde, kalici veritabani olarak da Neon.tech uzerinde 100% ucretsiz calisacak sekilde yapilandirilmistir.

| Bilesen | Platform | Gorev | Maliyet | Durum |
|---------|----------|-------|---------|-------|
| Frontend + Backend | Render.com | Web Service (React + Django + WhiteNoise) | Ucretsiz | Hazir |
| Veritabani | Neon.tech | PostgreSQL 16 + pgvector | Ucretsiz (Kalici) | TAMAMLANDI |
| Yapay Zeka | Google Gemini API | models/gemini-3.6-flash | Ucretsiz | TAMAMLANDI |

---

## YAPILANLAR (TAMAMLANAN ADIMLAR)

- [x] Neon.tech PostgreSQL projesi olusturuldu (cold-term-69679830).
- [x] Tum migration'lar Neon uzerinde calistirildi ve pgvector tablolari olusturuldu.
- [x] 20 kahve ve all-MiniLM-L6-v2 embedding vektorleri Neon veritabanina yuklendi (seed_coffees).
- [x] Django Admin kullanicisi olusturuldu (admin / admin123).
- [x] Google Gemini API entegrasyonu yapildi (generator.py).
- [x] Gemini 3.6 Flash ile ucuca RAG testi basariyla tamamlandi.
- [x] React frontend derlendi (frontend/dist/) ve Django WhiteNoise ile tek servis altinda birlestirildi.
- [x] build.sh scripti olusturuldu.

---

## KALAN ADIMLAR (SIMDI YAPILACAKLAR)

### Adim 1: Kodu GitHub'a Push Edin
Kendi terminalinizden calistirin:
```powershell
git add .
git commit -m "feat: Serve React frontend directly from Django via WhiteNoise"
git push origin main
```

### Adim 2: Render.com'da Servisi Baslatin
1. dashboard.render.com adresine gidin.
2. New + -> Web Service -> BrewMind reponuzu secin (Connect).
3. Ayarlari girin:
   - Name: brewmind
   - Region: Frankfurt (EU Central)
   - Branch: main
   - Root Directory: backend
   - Runtime: Python 3
   - Build Command: ./build.sh
   - Start Command: gunicorn config.wsgi:application
   - Instance Type: Free (0$/mo)
4. Environment Variables ekleyin:
   - DATABASE_URL = (Neon Dashboard'dan aldiginiz baglanti linki)
   - LLM_PROVIDER = GEMINI
   - GEMINI_API_KEY = (Google AI Studio'dan aldiginiz anahtar)
   - GEMINI_MODEL = models/gemini-3.6-flash
   - DEBUG = False
   - SECRET_KEY = django-insecure-prod-brewmind-secret-key-994829
   - ALLOWED_HOSTS = *
5. Deploy Web Service butonuna basin.

Render 2-3 dakika icinde derlemeyi tamamlayacak ve tek bir link (https://brewmind.onrender.com) ile hem web sitenizi hem de Gemini yapay zekasini yayina alacaktir.
