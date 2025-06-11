# Impor library yang dibutuhkan
import yt_dlp
from datetime import datetime
import csv # Impor modul CSV untuk menulis file

# --- KONFIGURASI ---
# URL dari kanal YouTube yang ingin diambil datanya
CHANNEL_URL = "https://www.youtube.com/@TimothyRonald/videos"
# Nama file output
OUTPUT_CSV_FILE = "hasil_scraping_video.csv"

def get_long_videos_with_ytdlp(channel_url):
    """
    Fungsi ini mengambil daftar video dari sebuah URL kanal YouTube
    menggunakan yt-dlp, lalu menyaring video berdurasi panjang.
    """
    
    # Opsi untuk yt-dlp (Langkah 1: Pengambilan Cepat)
    ydl_opts_flat = {
        'skip_download': True,
        'extract_flat': True,
        'quiet': True,
    }

    long_video_entries = []
    print("1. Mengambil daftar video dari kanal untuk penyaringan awal...")

    # Gunakan yt-dlp untuk mengekstrak informasi dasar
    with yt_dlp.YoutubeDL(ydl_opts_flat) as ydl:
        try:
            channel_info = ydl.extract_info(channel_url, download=False)
            
            if 'entries' in channel_info:
                # Saring video berdasarkan durasi > 60 detik
                for entry in channel_info['entries']:
                    if entry.get('duration') and entry['duration'] > 60:
                        long_video_entries.append(entry)
            
        except yt_dlp.utils.DownloadError as e:
            print(f"!!! Terjadi error saat mengambil daftar video: {e}")
            return []

    if not long_video_entries:
        print("Tidak ditemukan video berdurasi panjang pada pengambilan awal.")
        return []

    print(f"2. Ditemukan {len(long_video_entries)} video panjang. Mengambil detail lengkap...")
    
    long_videos_detailed = []
    # Opsi untuk yt-dlp (Langkah 2: Pengambilan Detail)
    ydl_opts_detailed = {
        'skip_download': True,
        'quiet': True,
    }

    # Loop melalui video yang sudah disaring untuk mendapatkan detail lengkap
    with yt_dlp.YoutubeDL(ydl_opts_detailed) as ydl:
        for entry in long_video_entries:
            try:
                # Ambil info lengkap untuk satu video berdasarkan ID
                video_id = entry.get('id')
                detailed_info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)

                # Ekstrak tanggal dari format 'YYYYMMDD' yang lebih andal
                release_date_str = detailed_info.get('upload_date')
                if release_date_str:
                    formatted_date = datetime.strptime(release_date_str, '%Y%m%d').strftime('%m/%d/%Y')
                else:
                    formatted_date = "N/A"
                
                video_data = {
                    "release_date": formatted_date,
                    "title": detailed_info.get('title', 'N/A'),
                    "channel_name": detailed_info.get('channel', 'N/A'),
                    "url": detailed_info.get('webpage_url', 'N/A')
                }
                long_videos_detailed.append(video_data)
            except Exception as e:
                print(f"Gagal mengambil detail untuk video ID {entry.get('id')}: {e}")

    return long_videos_detailed

# Bagian utama untuk menjalankan skrip
if __name__ == "__main__":
    videos = get_long_videos_with_ytdlp(CHANNEL_URL)
    
    if videos:
        print(f"\n--- MENYIMPAN {len(videos)} VIDEO KE FILE CSV ---")
        
        # Tentukan header untuk file CSV
        headers = ["release_date", "title", "channel_name", "url"]
        
        try:
            # Buka file CSV untuk ditulis
            with open(OUTPUT_CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                
                # Tulis baris header
                writer.writeheader()
                
                # Tulis semua data video
                writer.writerows(videos)
            
            print(f"\n✅ Sukses! Data telah disimpan ke dalam file: {OUTPUT_CSV_FILE}")
        except Exception as e:
            print(f"\n❌ Gagal menyimpan file CSV. Error: {e}")
        
        #Hitung Total Views untuk tiap video#
        total_views = sum(video['view_count'] for video in videos)
        #cetak hasil hitung total penonton#
        print(f"\💡 Total Views untuk semua video: {total_views}")


    else:
        print("\nTidak ada video yang ditemukan atau terjadi error.")
