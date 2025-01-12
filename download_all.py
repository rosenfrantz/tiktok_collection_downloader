import os
import csv
import re
import time
import yt_dlp

WAIT_SECS = 3

# Function to sanitize filenames for saving
def sanitize_filename(filename):
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in filename)

# Function to extract username and video ID from the URL
def extract_username_and_video_id(video_url):
    match = re.search(r"https://www\.tiktok\.com/@([\w\.\-]+)/video/(\d+)", video_url)
    if match:
        username, video_id = match.groups()
        return username, video_id
    return "unknown_user", "unknown_id"

# Function to download a single video
def download_video(collection_name, video_url, video_title, base_output_path):
    # Extract username and video ID
    username, video_id = extract_username_and_video_id(video_url)

    # Create the collection folder if it doesn't exist
    collection_folder = os.path.join(base_output_path, collection_name)
    os.makedirs(collection_folder, exist_ok=True)

    # Sanitize the video title to use as part of the filename
    sanitized_title = sanitize_filename(video_title)
    if not sanitized_title:
        sanitized_title = "Untitled"

    # Construct the output filename
    output_filename = f"{username}_{sanitized_title}_{video_id}.mp4"
    output_file = os.path.join(collection_folder, output_filename)

    # Skip download if the file already exists
    if os.path.exists(output_file):
        print(f"Skipping download, file already exists: {output_file}")
        return

    ydl_opts = {
        'outtmpl': output_file,  # Use the constructed filename
        'format': 'best',
        'noplaylist': True,
        'quiet': False,
        'extractor_args': {'tiktok': {'webpage_download': True}},
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            print(f"Video successfully downloaded to {output_file}")
    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading video ({video_url}): {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred while downloading ({video_url}): {str(e)}")

# Function to process the CSV file and download videos
def process_csv_and_download(csv_file_path, base_output_path):
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                collection_name = row['Collection Name']
                video_url = row['TikTok Video URL']
                video_title = row['Video Title']
                download_video(collection_name, video_url, video_title, base_output_path)
                time.sleep(WAIT_SECS)
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file_path}")
    except KeyError as e:
        print(f"Missing column in CSV file: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

# Path to the CSV file and output directory
csv_file = "tiktok_video_info.csv"  # Replace with your CSV file path
output_directory = "videos"  # Replace with your base output folder path

# Process the CSV and download videos
process_csv_and_download(csv_file, output_directory)
