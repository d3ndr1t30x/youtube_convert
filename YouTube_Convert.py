from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime
import re

def sanitize_title(title):
    # Remove any invalid characters from the title
    return re.sub(r'[\\/*?:"<>|]', "_", title)

def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return "\n".join([f"[{item['start']:.2f}] {item['text']}" for item in transcript])
    except Exception as e:
        return f"Error fetching transcript: {e}"

def save_transcript_to_file(url):
    try:
        yt = YouTube(url)
        title = yt.title
        video_id = yt.video_id
        sanitized_title = sanitize_title(title)
        
        transcript = fetch_transcript(video_id)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{sanitized_title}_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(transcript)
        
        print(f"Transcript saved to {filename}")
    except Exception as e:
        print(f"Error: {e}")

def print_help():
    print("""
Usage: python youtube_transcript_downloader.py

This script downloads the transcript of a YouTube video and saves it to a text file.
You will be prompted to enter a YouTube video URL.

Options:
    -h, --help          Display this help message
    -q, --quit          Quit the script
""")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print_help()
            sys.exit(0)
        elif sys.argv[1] in ['-q', '--quit']:
            sys.exit(0)
        else:
            print("Invalid option. Use -h or --help for usage instructions.")
            sys.exit(1)
    
    url = input("Enter YouTube URL: ")
    save_transcript_to_file(url)
