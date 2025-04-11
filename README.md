# ai-hr-system
Yapay Zeka Destekli İnsan Kaynakları Projesi
Bu proje, CV ve iş ilanı metinlerini analiz ederek yapay zekâ ile **uyumluluk skoru** hesaplayan bir insan kaynakları destek sistemidir.  
Geliştirme süreci bir Django tabanlı web arayüzü üzerine entegre edilerek ilerlemektedir.

---

## ✨ Bu repoda ne var?

📦 `matcher.py`:  
TF-IDF + Cosine Similarity kullanarak CV ile iş ilanı arasında eşleştirme skoru hesaplar.

🌐 `main.py`:  
FastAPI kullanılarak geliştirilen REST API — dışarıdan gelen metinleri alır, skoru döner.

🐳 `Dockerfile`:  
Projeyi herkesin bilgisayarında aynı şekilde çalıştırmak için taşınabilir hale getirir.

---

## 💻 Kullanım

### 1. Docker ile başlat:

```bash
docker build -t ai-hr-api .
docker run -d -p 8000:8000 ai-hr-api
API'yi test etmek için tarayıcıya git:
bash
Kodu kopyala
http://localhost:8000/docs

{
  "cv_text": "Python, Django, REST",
  "job_text": "Looking for a Python backend developer"
}
