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

# BOLUM 4: BULUTA CIKIS (CANLI SISTEM: RENDER + NEON + GEMINI)

Proje tek bir servis olarak Render.com uzerinde, kalici veritabani olarak Neon.tech uzerinde 100% ucretsiz ve 7/24 calisir durumdadir.

- **Canli Web Sitesi:** https://brewmind.onrender.com
- **Canli Admin Paneli:** https://brewmind.onrender.com/admin/

| Bilesen | Platform | Gorev | Maliyet | Durum |
|---------|----------|-------|---------|-------|
| Frontend + Backend | Render.com | Web Service (React + Django + WhiteNoise) | Ucretsiz | CANLIDA (Aktif) |
| Veritabani | Neon.tech | PostgreSQL 16 + pgvector | Ucretsiz (Kalici) | CANLIDA (Aktif) |
| Yapay Zeka | Google Gemini API | models/gemini-3.6-flash | Ucretsiz | CANLIDA (Aktif) |

---

## KRITIK MUHENDISLIK VE PERFORMANS COZUMLERI

1. **Tek Servis Mimarisi (WhiteNoise):**
   - Vercel'in 500 MB'lik sunucusuz fonksiyon sinirini asmak ve iki ayri alan adi / CORS karmasasini onlemek icin React arayuzu `npm run build` ile derlendi.
   - Django `settings.py` icinde `WhiteNoise` ve `TEMPLATES` ile dogrudan Django uzerinden sunuldu.
   - `urls.py` icindeki SPA yonlendirmesi ile tum sayfalar (`/`, `/dashboard`) ayni domain uzerinden acilmaktadir.

2. **Hafif CPU-only PyTorch:**
   - Standart Linux `torch` kurulumu 2.5 GB'lik gereksiz NVIDIA CUDA suruculerini indirdigi icin `build.sh` icinde CPU surumu (`--index-url https://download.pytorch.org/whl/cpu torch`) kuruldu.
   - RAM kullanimi ~700 MB'tan ~80 MB'a, indirme boyutu 2.5 GB'tan 150 MB'a dusuruldu.

3. **Tembel Yukleme (Lazy Loading):**
   - `sentence-transformers` ve model kutuphaneleri sunucu baslarken degil, sadece kullanici ilk arama yaptiginda yuklenecek sekilde ayarlandi.
   - Sunucu acilis suresi 35 saniyeden 1 saniyenin altina indi.

4. **Derleme Aninda Model On-Indirme (Build-time Pre-download):**
   - `all-MiniLM-L6-v2` embedding modeli `build.sh` calisirken disk onbellegine indirildi. Arama anindaki ag indirme gecikmeleri onlendi.

5. **Gunicorn Timeout (120s):**
   - Gunicorn sunucusunun varsayilan 30 saniyelik siniri `--timeout 120` olarak artirildi, boylece ilk yuklemedeki zaman asimi hatalari tamamen engellendi.

---

## TAMAMLANAN DEPLOYMENT ADIMLARI

- [x] Neon.tech PostgreSQL projesi olusturuldu (cold-term-69679830).
- [x] Tum migration'lar Neon uzerinde calistirildi ve pgvector tablolari olusturuldu.
- [x] 20 kahve ve all-MiniLM-L6-v2 embedding vektorleri Neon veritabanina yuklendi (seed_coffees).
- [x] Django Admin kullanicisi olusturuldu (admin / admin123).
- [x] Google Gemini API entegrasyonu yapildi (generator.py - models/gemini-3.6-flash).
- [x] React frontend derlendi (frontend/dist/) ve Django WhiteNoise ile tek servis altinda birlestirildi.
- [x] CPU-only PyTorch ve Lazy Loading bellek optimizasyonlari uygulandi.
- [x] build.sh derleme scripti hazirlandi.
- [x] Render.com uzerinde Web Service kuruldu ve basariyla canliya alindi.
- [x] Canli test: Arayuz, 20 kahve listesi, RAG vektor aramasi ve Gemini barista onerileri dogrulandi.
