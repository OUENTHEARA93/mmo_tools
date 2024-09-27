import logging

import yt_dlp
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from flask_sqlalchemy.pagination import Pagination
from flask_migrate import Migrate

from models import db, FacebookAccount

# Configure database

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

BASE_FOLDER_PATH = 'D:\\2024_Content Editor'

db.init_app(app)


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


@app.route('/')
def index():
    return render_template('index.html')


@app.before_request
def create_tables():
    db.create_all()


@app.route('/device')
def device():
    return render_template('/device/devices.html')


# GMAIL MANAGEMENT
@app.route('/gmail')
def gmail(page=1):
    return render_template('/gmail/accounts.html')


@app.route('/website')
def website(page=1):
    return render_template('/website/pages.html')


# View Item
@app.route("/facebook/register")
def facebook_register():
    return render_template("/facebook/register.html")


@app.route('/facebook')
@app.route('/facebook/page/<int:page>')
def facebook(page=1):
    per_page = 10  # Number of items per page
    pagination = FacebookAccount.query.order_by(FacebookAccount.followers.desc()).paginate(page=page, per_page=per_page,
                                                                                           error_out=False)

    if page > pagination.pages or page < 1:
        flash('Invalid page number', 'error')
        return redirect(url_for('facebook'))

    return render_template('/facebook/pages.html', items=pagination.items, pagination=pagination)


# View Item
@app.route("/view/<int:id>")
def view_item(id):
    account = FacebookAccount.query.get_or_404(id)
    return render_template("/facebook/view_page.html", item=account)


@app.route('/add_account2', methods=['POST'])
def add_account():
    account = request.form.get('account')
    page_name = request.form.get('page_name')
    followers = request.form.get('followers')
    reached = request.form.get('reached')
    page_url = request.form.get('page_url')
    created_date = request.form.get('created_date')
    monetization = request.form.get('monetization')
    description = request.form.get('description')

    new_account = FacebookAccount(account=account, page_name=page_name, followers=followers,
                                  reached=reached, page_url=page_url, created_date=created_date,
                                  monetization=monetization, description=description)
    db.session.add(new_account)
    db.session.commit()
    return redirect(url_for('facebook'))


@app.route("/facebook/addpage")
# @app.route('/facebook')
@app.route('/facebook/addpage/page/<int:page>')
def load_create_page(page=1):
    per_page = 10  # Number of items per page
    pagination = FacebookAccount.query.order_by(FacebookAccount.followers.desc()).paginate(page=page, per_page=per_page,
                                                                                           error_out=False)

    if page > pagination.pages or page < 1:
        flash('Invalid page number', 'error')
        return redirect(url_for('facebook'))

    return render_template('/facebook/add_pages.html', items=pagination.items, pagination=pagination)


@app.route('/add_account', methods=['POST'])
def add_page():
    account = request.form.get('account')
    page_name = request.form.get('page_name')
    followers = request.form.get('followers')
    reached = request.form.get('reached')
    page_url = request.form.get('page_url')
    created_date = request.form.get('created_date')
    monetization = request.form.get('monetization')
    description = request.form.get('description')

    new_account = FacebookAccount(account=account, page_name=page_name, followers=followers,
                                  reached=reached, page_url=page_url, created_date=created_date,
                                  monetization=monetization, description=description)
    db.session.add(new_account)
    db.session.commit()
    return redirect(url_for('load_create_page'))


# Edit Item
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_item(id):
    item = FacebookAccount.query.get_or_404(id)
    if request.method == "POST":
        item.account = request.form['account']
        item.page_name = request.form['page_name']

        item.followers = request.form['followers']
        item.reached = request.form['reached']
        item.created_date = datetime.strptime(request.form['created_date'], '%Y-%m-%d')
        item.monetization = request.form['monetization']
        item.description = request.form['description']
        # update other fields similarly
        db.session.commit()
        flash("Item updated successfully!", "success")
        return redirect(url_for('facebook'))  # Redirect to the main page after editing

    return render_template("/facebook/edit_page_item.html", item=item)


# Delete Item
@app.route("/facebook/addpage/delete/<int:id>", methods=["POST"])
def delete_item(id):
    item = FacebookAccount.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash("Item deleted successfully!", "success")
    return redirect(url_for('load_create_page'))


# Route for Adding New Account
@app.route('/add_gmail_account', methods=['POST'])
def add_gmail_account():
    return redirect(url_for('gmail'))


@app.route('/instagram')
def instagram(page=1):
    return render_template('/instagram/accounts.html')


@app.route('/threads')
def threads(page=1):
    return render_template('/threads/accounts.html')


@app.route('/tiktok')
def tiktok(page=1):
    return render_template('/tiktok/accounts.html')


@app.route('/youtube')
def youtube(page=1):
    return render_template('/youtube/channels.html')


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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




@app.route('/scrape_videos', methods=['POST'])
def scrape_videos():
    video_links = request.json.get('video_links')
    video_data = []

    for link in video_links:
        video_info = fetch_video_info(link)
        video_data.append(video_info)

    return jsonify(video_data)


@app.route('/content')
@app.route('/content/page/<int:page>')
def content(page=1):
    files = get_files_and_folders(BASE_FOLDER_PATH)
    return render_template('/content/contents.html', files=files)

@app.route('/content/edit/1')
def edit_content(page=1):
    # files = get_files_and_folders(BASE_FOLDER_PATH)
    return render_template('/content/edit_content.html')

@app.route('/filter', methods=['POST'])
def filter_files():
    folder_name = request.form.get('folderName')
    search_keyword = request.form.get('keyword')

    # Apply filters based on user input
    files = get_files_and_folders(BASE_FOLDER_PATH, folder_name, search_keyword)

    return render_template('/content/contents.html', files=files)


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


@app.route('/download', methods=['POST'])
def download():
    save_as = request.form.get('savefile')
    video_size = request.form.get('video_size')
    folder_name = request.form.get('folderName')
    video_links = request.form.get('videoLinks').strip().split('\n')

    download_path = os.path.join('downloads', folder_name)
    os.makedirs(download_path, exist_ok=True)

    # Configure yt-dlp options based on user input
    ydl_opts = {
        'format': f'bestvideo[height<={video_size}]+bestaudio/best[height<={video_size}]',
        'outtmpl': os.path.join(download_path, f'%(title)s.%(ext)s'),
        'retries': 10,
        'socket_timeout': 30,
        'noprogress': True,  # Disable progress reporting
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3' if save_as == 'MP3' else 'mp4',
        }] if save_as == 'MP3' else []  # Ensure postprocessors is an empty list if not 'MP3'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download(video_links)
        except yt_dlp.utils.DownloadError as e:
            print(f"Skipping video {video_links} due to error: {e}")

    return jsonify({'message': 'Download started, check server for output'})


@app.route('/editor')
def editor(page=1):
    return render_template('/content/editor.html')


@app.route('/facebook/accounts')
def facebook_accounts():
    return render_template('/facebook/accounts.html')


@app.route('/facebook/post-reels')
def facebook_reels():
    return render_template('/facebook/post_reels.html')


@app.route('/telegram/channel')
def telegram_channels():
    return render_template('/telegram/channels.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()  # Ensure the database tables are created inside the application context
    app.run(debug=True, host='0.0.0.0')
