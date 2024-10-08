import os

import yt_dlp

from myapp import app

# Utility function to format file sizes
def format_file_size(size_in_bytes):
    """Format the file size from bytes to MB or GB."""
    if size_in_bytes == 0 or size_in_bytes is None:
        return "Unknown"
    size_in_mb = size_in_bytes / (1024 * 1024)
    if size_in_mb < 1024:
        return f"{size_in_mb:.2f} MB"
    else:
        size_in_gb = size_in_mb / 1024
        return f"{size_in_gb:.2f} GB"

@app.context_processor
def utility_processor():
    def format_number(num):
        if num >= 1_000_000:
            return f'{num / 1_000_000:.1f}M'
        elif num >= 1_000:
            return f'{num / 1_000:.1f}K'
        else:
            return str(num)

    return dict(format_number=format_number)


def format_views(count):
    if count < 1000:
        return str(count)
    elif count < 1000000:
        return f"{count // 1000}K"
    else:
        return f"{count // 1000000}M"


def fetch_video_info(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,  # We're only getting the info, not downloading the video
        'force_generic_extractor': False
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)

            duration_minutes = round(info.get('duration', 0) / 60, 2)
            views = info.get('view_count', 0) if info.get('view_count') is not None else 0
            formatted_views = format_views(views)
            return {
                'title': info.get('title', ''),
                'description': info.get('description', ''),
                'duration': duration_minutes,  # info.get('duration', 0),
                'views': f"{formatted_views}",
                'size': info.get('filesize', 0),
                'path': '/path/to/video'  # You can customize the path
            }
        except yt_dlp.utils.DownloadError as e:
            print(f"Skipping video {url} due to error: {e}")


def get_files_and_folders(base_path, folder_name=None, search_keyword=None):
    """Fetch all files and folders from the directory."""
    folder_list = []

    for folder_name, subfolders, files in os.walk(base_path):
        folder_info = {
            'name': os.path.basename(folder_name),
            'path': folder_name,
            'status': 'Active',  # You can modify this based on your logic
            'size': '30G',  # sum(os.path.getsize(os.path.join(folder_name, f)) for f in files),
            # Total size of files in the folder
            'videos': '50K',  # len([f for f in files if f.endswith(('.mp4', '.mkv', '.avi'))]),
            'photos': '10K',  # len([f for f in files if f.endswith(('.jpg', '.png', '.jpeg'))]),
            'description': 'Folder description'  # Customize as per requirement
        }
        # if (not folder_name or folder_name.lower() in folder_info['name'].lower()) and \
        #         (not search_keyword or search_keyword.lower() in folder_info['name'].lower()):
        folder_list.append(folder_info)

    return folder_list
