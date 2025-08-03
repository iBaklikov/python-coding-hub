# file: youtube_single_format_download.py

from yt_dlp import YoutubeDL

def download_youtube_video(url: str, output_path: str) -> None:
    options = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # fallback to non-mergeable mp4
        'merge_output_format': 'mp4',  # only relevant if ffmpeg exists
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'noplaylist': True,
        'postprocessors': [],  # disable all postprocessing to avoid ffmpeg
        'verbose': True,
        'quiet': False,
        'no_warnings': True,
    }

    with YoutubeDL(options) as ydl:
        ydl.download([url])

# example usage
if __name__ == '__main__':
    video_url = 'https://www.youtube.com/watch?v=4y9wCASRqak'
    output_path = 'downloads'
    download_youtube_video(video_url, output_path)
