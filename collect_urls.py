import os
import re
import csv
from bs4 import BeautifulSoup

def extract_video_info_from_html(file_path):
    """Extract TikTok video URLs and titles from an HTML file."""
    video_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')

        # Regex pattern for TikTok video URLs
        video_pattern = re.compile(r"https://www\.tiktok\.com/@[\w\.\-]+/video/\d+")
        videos = soup.find_all("a", href=video_pattern)

        for video in videos:
            url = video['href']
            raw_title = video.get('title', 'Untitled')
            title = process_title(raw_title)
            video_data.append((url, title))
    return video_data

def process_title(raw_title):
    """Process video title by removing hashtags and limiting length."""
    # Remove hashtags using regex
    title_without_hashtags = re.sub(r"#\S+", "", raw_title).strip()
    # Limit title to 256 characters
    return title_without_hashtags[:256]

def process_html_folder(folder_path, output_csv):
    """Process all HTML files in a folder and save the extracted video info to a CSV."""
    # Use dictionary to store unique URLs with their data
    url_dict = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            collection_name = os.path.splitext(filename)[0]
            file_path = os.path.join(folder_path, filename)
            video_info = extract_video_info_from_html(file_path)
            for url, title in video_info:
                # Only update if URL doesn't exist or current title is better
                if url not in url_dict or (not url_dict[url][1] and title):
                    url_dict[url] = (collection_name, title)

    # Convert dictionary back to list for CSV writing
    data = [[collection_name, url, title] 
            for url, (collection_name, title) in url_dict.items()]

    # Write data to a CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Collection Name", "TikTok Video URL", "Video Title"])
        writer.writerows(data)

    print(f"Extracted video info has been saved to {output_csv}")

# Folder containing HTML files and the output CSV file
input_folder = "collection_htmls"  # Replace with your folder path
output_csv_file = "tiktok_video_info.csv"

process_html_folder(input_folder, output_csv_file)
