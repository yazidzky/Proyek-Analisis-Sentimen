# Proyek Analisis Sentimen Play Store (Indonesia)

Proyek ini melakukan analisis sentimen untuk ulasan aplikasi Google Play (bahasa Indonesia) menggunakan pendekatan **lexicon-based labeling** dan model **machine learning (TF-IDF + LinearSVC)**.

## Fitur

- Scraping ulasan Google Play via `google-play-scraper`.
- Label sentimen otomatis memakai lexicon (kamus positif/negatif sederhana).
- Training model berbasis:
  - **Word TF-IDF** (ngram 1–2)
  - **Char TF-IDF** (ngram 3–5)
- Model disimpan sebagai `models/sentiment_playstore.joblib`.

## Struktur Folder

- `scrape_playstore.py` : skrip pengambilan ulasan + labeling lexicon sederhana.
- `playstore_reviews.csv` : dataset ulasan (contoh/sumber data).
- `train_sentiment.ipynb` : notebook training (download lexicon, bersih teks, training model).
- `models/`:
  - `sentiment_playstore.joblib` : model terlatih.
  - `metrics.txt` : metrik akurasi (dari training).

## Requirements

Lihat `requirements.txt`.

## Setup Environment

Disarankan membuat environment Python terlebih dulu, lalu instal dependensi:

```bash
pip install -r requirements.txt
```

## 1) Scraping Ulasan & Buat Dataset

Jalankan:

```bash
python scrape_playstore.py --apps com.whatsapp com.instagram.android com.snapchat.android --per_app 1200 --lang id --country id --out data/playstore_reviews.csv
```

Keterangan:

- `--apps` : daftar app id Google Play
- `--per_app` : target jumlah ulasan per aplikasi
- `--lang`/`--country` : parameter language dan country
- `--out` : path output CSV

> Catatan: pada skrip, output default `--out data/playstore_reviews.csv` (jika folder `data/` belum ada akan dibuat).

## 2) Training Model

Training dilakukan di `train_sentiment.ipynb`.

Di notebook:

- Download lexicon InSet (positive/negative) dan kamus alay.
- Cleaning teks + normalisasi slang.
- Label ulang dengan skor lexicon.
- Latih model `LinearSVC` pada gabungan fitur word+char.
- Simpan model ke `models/sentiment_playstore.joblib` dan metrik ke `models/metrics.txt`.

Cara menjalankan notebook:

```bash
jupyter notebook
```

Lalu buka `train_sentiment.ipynb` dan jalankan cell.

## 3) Prediksi Sentimen (Contoh)

Di notebook/script, fungsi prediksi memakai pipeline yang sama dengan training:

```python
predict_sentiment("Aplikasi ini sangat bagus dan mudah digunakan")
predict_sentiment("Sering error dan lemot")
predict_sentiment("Biasa saja, tidak terlalu istimewa")
```

## Catatan

- Label sentimen yang digunakan bersifat **rule/lexicon-based**, jadi performa model akan mengikuti kualitas lexicon dan data ulasan.
- Dataset yang lebih besar/lebih beragam umumnya meningkatkan kualitas model.
