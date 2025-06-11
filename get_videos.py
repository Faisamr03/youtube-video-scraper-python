# Impor library yang dibutuhkan
import os
from datetime import datetime
from googleapiclient.discovery import build
from isodate import parse_duration

# --- KONFIGURASI ---
# Ganti dengan API Key yang sudah Anda buat dari Google Cloud Console
API_KEY = "AIzaSyBqZy0iMgQ31qX8ZKcz4aWffyuMBf8yINs"

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
        channel_request = youtube.channels().list(
            part="contentDetails,snippet",
            id=channel_id
        )
        channel_response = channel_request.execute()

        # --- PENANGANAN ERROR BARU ---
        # Periksa apakah respons dari Google mengandung pesan error
        if 'error' in channel_response:
            print("\n!!! TERJADI ERROR DARI API GOOGLE !!!")
            error_details = channel_response['error']['errors'][0]
            print(f"   Pesan: {error_details.get('message')}")
            print(f"   Alasan: {error_details.get('reason')}")
            return []

        # Periksa apakah 'items' kosong, yang berarti channel tidak ditemukan
        if not channel_response.get("items"):
            print("!!! Channel tidak ditemukan atau tidak ada data yang dikembalikan untuk ID tersebut.")
            return []
        
        # Jika lolos pengecekan, lanjutkan seperti biasa
        channel_item = channel_response["items"][0]
        uploads_playlist_id = channel_item["contentDetails"]["relatedPlaylists"]["uploads"]
        channel_title = channel_item["snippet"]["title"]
    
    except Exception as e:
        # Menangkap error lain yang mungkin terjadi
        print(f"\n!!! ERROR TIDAK TERDUGA SAAT MENGAMBIL INFO CHANNEL !!!")
        print(f"   Detail: {e}")
        return []

    video_ids = []
    next_page_token = None
    print("2. Mengumpulkan semua ID video dari channel. Ini mungkin butuh waktu...")
    # ... (Sisa kode tidak berubah)
    while True:
        playlist_request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        playlist_response = playlist_request.execute()

        for item in playlist_response["items"]:
            video_ids.append(item["contentDetails"]["videoId"])

        next_page_token = playlist_response.get("nextPageToken")
        if not next_page_token:
            break
            
    print(f"Total ditemukan {len(video_ids)} video. Memproses detail...")

    long_videos = []
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i+50]
        video_details_request = youtube.videos().list(
            part="snippet,contentDetails",
            id=",".join(chunk)
        )
        video_details_response = video_details_request.execute()

        for item in video_details_response["items"]:
            duration_iso = item["contentDetails"]["duration"]
            duration_seconds = parse_duration(duration_iso).total_seconds()

            if duration_seconds > 60:
                published_str = item["snippet"]["publishedAt"]
                release_date_obj = datetime.fromisoformat(published_str.replace('Z', '+00:00'))
                formatted_date = release_date_obj.strftime('%m/%d/%Y')

                video_info = {
                    "release_date": formatted_date,
                    "title": item["snippet"]["title"],
                    "channel_name": channel_title,
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
        
        for index, video in enumerate(videos):
            print(f"\n--- Video #{index + 1} ---")
            print(f"A. Tanggal Rilis: {video['release_date']}")
            print(f"B. Judul: {video['title']}")
            print(f"C. Nama Kanal: {video['channel_name']}")
            print(f"D. URL: {video['url']}")
