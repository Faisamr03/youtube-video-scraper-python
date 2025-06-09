Scraper Video YouTube dengan Python
Ini adalah sebuah skrip Python sederhana yang berfungsi untuk melakukan scraping data dari video-video di sebuah kanal YouTube. Skrip ini menggunakan yt-dlp untuk mengambil metadata video, menyaringnya untuk mendapatkan video utama (bukan Shorts), dan menyimpannya ke dalam sebuah file CSV.

Proyek ini dibuat sebagai latihan untuk mengasah kemampuan dalam pengumpulan data web, pengolahan data dengan Python, dan otomatisasi.

## Fitur Utama
Scraping Kanal: Mengambil daftar lengkap video dari URL kanal YouTube yang ditentukan.

Filter Video Shorts: Secara otomatis menyaring dan membuang video dengan durasi di bawah 60 detik.

Ekstraksi Data Lengkap: Mengambil informasi detail untuk setiap video utama, termasuk:

Tanggal Rilis

Judul Video

Nama Kanal

URL Video

Jumlah Views

Jumlah Likes

Output ke CSV: Menyimpan semua data yang berhasil diambil ke dalam sebuah file .csv yang rapi dan mudah diolah lebih lanjut di Excel atau Google Sheets.

## Teknologi yang Digunakan
Python: Bahasa pemrograman utama yang digunakan.

yt-dlp: Sebuah command-line program yang sangat andal untuk mengambil informasi dan konten video dari YouTube dan situs lainnya.

## Persyaratan
Pastikan Anda memiliki Python 3 terinstal di komputer Anda. Selain itu, Anda perlu menginstal library yt-dlp.

Buka terminal atau command prompt Anda dan jalankan perintah berikut:

pip install yt-dlp

## Cara Penggunaan
Kloning Repositori

git clone https://github.com/Faisamr03/youtube-video-scraper-python.git
cd youtube-video-scraper-python

Konfigurasi Kanal
Buka file skrip Python (.py) Anda. Ubah nilai variabel CHANNEL_URL dengan URL kanal YouTube yang ingin Anda scraping. Pastikan URL mengarah ke tab "Videos".

# URL dari kanal YouTube yang ingin diambil datanya
CHANNEL_URL = "https://www.youtube.com/@NamaKanal/videos"

Jalankan Skrip
Buka terminal di dalam folder proyek dan jalankan perintah berikut:

python nama_file_anda.py

Lihat Hasilnya
Setelah skrip selesai berjalan, sebuah file baru bernama hasil_scraping_video.csv akan dibuat di dalam folder yang sama. File ini berisi semua data video yang berhasil di-scraping.
