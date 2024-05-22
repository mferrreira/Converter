import yt_dlp

class YouTubeDownloader:
    def __init__(self):
        pass

    def download_video(self, url, output_path, convert_to):
        try:
            ydl_opts = {
                'format': 'bestaudio/best' if 'mp3' in convert_to else 'best',
                'outtmpl': f'{output_path}/%(title)s.%(ext)s',
                'merge_output_format': 'mkv' if 'mp3' in convert_to else 'mp4',
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                downloaded_files = [f"{output_path}/{info['title']}.{format}" for format in convert_to]
                return downloaded_files
        except yt_dlp.DownloadError as e:
            print(f"Erro ao baixar o vídeo do YouTube: {e}")
            return False
