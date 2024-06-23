import tkinter as tk
from tkinter import messagebox
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
        
        messagebox.showinfo("Success", f"Transcript saved to {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

def download_transcript():
    url = url_entry.get()
    if url:
        save_transcript_to_file(url)
    else:
        messagebox.showwarning("Warning", "Please enter a YouTube URL.")

# GUI Setup
root = tk.Tk()
root.title("YouTube Transcript Downloader")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# URL Entry
url_label = tk.Label(frame, text="Enter YouTube URL:")
url_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
url_entry = tk.Entry(frame, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)

# Download Button
download_button = tk.Button(frame, text="Download Transcript", command=download_transcript)
download_button.grid(row=1, columnspan=2, pady=10)

# Start the GUI main loop
root.mainloop()
