# Impor library yang dibutuhkan
import os
from datetime import datetime
from googleapiclient.discovery import build
from isodate import parse_duration

# --- KONFIGURASI ---
# Ganti dengan API Key yang sudah Anda buat dari Google Cloud Console
API_KEY = "UCXMB8OiiSnq2B4xLgUtTYhw"

# Channel ID untuk kanal Timothy Ronald
CHANNEL_ID = "UC90E33l_y3_S-d2T7aN5u2A" 

def get_long_videos(api_key, channel_id):
    """
    Fungsi ini mengambil daftar video dari sebuah channel YouTube,
    lalu menyaringnya untuk mendapatkan video berdurasi panjang (lebih dari 60 detik).
    """
    # Membangun koneksi ke layanan YouTube API
    youtube = build('youtube', 'v3', developerKey=api_key)

    print("1. Mengambil informasi channel untuk mendapatkan ID playlist dan nama kanal...")
    try:
        # Langkah pertama adalah mendapatkan detail channel, termasuk nama dan playlist 'uploads'
        channel_request = youtube.channels().list(
            # Tambahkan 'snippet' untuk mendapatkan nama kanal
            part="contentDetails,snippet",
            id=channel_id
        )
        channel_response = channel_request.execute()
        
        # Ekstrak detail yang dibutuhkan
        channel_item = channel_response["items"][0]
        uploads_playlist_id = channel_item["contentDetails"]["relatedPlaylists"]["uploads"]
        channel_title = channel_item["snippet"]["title"]
    except Exception as e:
        print(f"Error saat mengambil info channel: {e}")
        return []

    video_ids = []
    next_page_token = None
    print("2. Mengumpulkan semua ID video dari channel. Ini mungkin butuh waktu...")
    # Langkah kedua adalah mengambil semua ID video dari playlist 'uploads'
    while True:
        playlist_request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,  # Ambil 50 video per permintaan untuk efisiensi
            pageToken=next_page_token
        )
        playlist_response = playlist_request.execute()

        for item in playlist_response["items"]:
            video_ids.append(item["contentDetails"]["videoId"])

        # Cek jika ada halaman selanjutnya
        next_page_token = playlist_response.get("nextPageToken")
        if not next_page_token:
            break
            
    print(f"Total ditemukan {len(video_ids)} video. Memproses detail...")

    long_videos = []
    # Langkah ketiga, ambil detail video per 50 buah untuk efisiensi
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i+50]
        video_details_request = youtube.videos().list(
            part="snippet,contentDetails",
            id=",".join(chunk)
        )
        video_details_response = video_details_request.execute()

        # Langkah keempat, saring video dan format data
        for item in video_details_response["items"]:
            duration_iso = item["contentDetails"]["duration"]
            duration_seconds = parse_duration(duration_iso).total_seconds()

            if duration_seconds > 60:
                # Ambil tanggal rilis dalam format string ISO
                published_str = item["snippet"]["publishedAt"]
                # Ubah string ISO menjadi objek datetime, lalu format ulang
                # .replace('Z', '+00:00') diperlukan agar fromisoformat bisa bekerja
                release_date_obj = datetime.fromisoformat(published_str.replace('Z', '+00:00'))
                formatted_date = release_date_obj.strftime('%m/%d/%Y') # Format: MM/DD/YYYY

                video_info = {
                    "release_date": formatted_date,
                    "title": item["snippet"]["title"],
                    "channel_name": channel_title, # Tambahkan nama kanal
                    "url": f"https://www.youtube.com/watch?v={item['id']}"
                }
                long_videos.append(video_info)

    return long_videos

# Bagian utama untuk menjalankan skrip
if __name__ == "__main__":
    if API_KEY == "GANTI_DENGAN_API_KEY_ANDA":
        print("!!! PENTING: Harap ganti nilai variabel 'API_KEY' di dalam kode dengan kunci API Anda.")
    else:
        videos = get_long_videos(API_KEY, CHANNEL_ID)
        print(f"\n--- DITEMUKAN {len(videos)} VIDEO UTAMA (BUKAN SHORTS) ---")
        
        # Cetak hasil video yang sudah disaring dengan format baru
        for index, video in enumerate(videos):
            print(f"\n--- Video #{index + 1} ---")
            print(f"A. Tanggal Rilis: {video['release_date']}")
            print(f"B. Judul: {video['title']}")
            print(f"C. Nama Kanal: {video['channel_name']}")
            print(f"D. URL: {video['url']}")
