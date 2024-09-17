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
# @app.route('/instagram/page/<int:page>')
# @app.route('/page')
def device(page=1):
    # per_page = 10  # Number of items per page
    # pagination = GmailAccount.query.paginate(page=page, per_page=per_page, error_out=False)
    #
    # if page > pagination.pages or page < 1:
    #     flash('Invalid page number', 'error')
    #     return redirect(url_for('gmail'))
    #
    # return render_template('gmail.html', items=pagination.items, pagination=pagination)
    return render_template('device.html')


# GMAIL MANAGEMENT
@app.route('/gmail')
def gmail(page=1):
    # per_page = 10  # Number of items per page
    # pagination = GmailAccount.query.paginate(page=page, per_page=per_page, error_out=False)
    #
    # if page > pagination.pages or page < 1:
    #     flash('Invalid page number', 'error')
    #     return redirect(url_for('gmail'))
    #
    # return render_template('gmail.html', items=pagination.items, pagination=pagination)
    return render_template('gmail.html')


@app.route('/website')
# @app.route('/instagram/page/<int:page>')
# @app.route('/page')
def website(page=1):
    # per_page = 10  # Number of items per page
    # pagination = GmailAccount.query.paginate(page=page, per_page=per_page, error_out=False)
    #
    # if page > pagination.pages or page < 1:
    #     flash('Invalid page number', 'error')
    #     return redirect(url_for('gmail'))
    #
    # return render_template('gmail.html', items=pagination.items, pagination=pagination)
    return render_template('website.html')


@app.route('/facebook')
@app.route('/facebook/page/<int:page>')
def facebook(page=1):
    per_page = 10  # Number of items per page
    pagination = FacebookAccount.query.order_by(FacebookAccount.followers.desc()).paginate(page=page, per_page=per_page,
                                                                                           error_out=False)

    if page > pagination.pages or page < 1:
        flash('Invalid page number', 'error')
        return redirect(url_for('facebook'))

    return render_template('/facebook/page.html', items=pagination.items, pagination=pagination)


@app.route('/facebook/register')
def register_account():
    return render_template('/facebook/register_account.html')


@app.route('/facebook/post_reels')
def post_reels():
    return render_template('/facebook/post_reels.html')


#     return redirect(url_for('facebook'))
@app.route('/add_account', methods=['POST'])
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


# View Item
@app.route("/view/<int:id>")
def view_item(id):
    account = FacebookAccount.query.get_or_404(id)
    return render_template("/facebook/view_page.html", item=account)


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

    return render_template("edit_item.html", item=item)


# @app.route('/filter_data', methods=['GET'])
# def filter_data():
#     search = request.args.get('search', '')
#     category = request.args.get('category', '')
#
#     # Build the query based on filters
#     query = Account.query
#     if search:
#         query = query.filter(Account.account.like(f'%{search}%'))
#
#     if category:
#         query = query.filter_by(account=category)
#
#     # Retrieve the filtered data
#     items = query.all()
#
#     # Return the updated rows as part of the AJAX response
#     return render_template('page.html', items=items)


# Delete Item
@app.route("/delete/<int:id>", methods=["POST"])
def delete_item(id):
    item = FacebookAccount.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash("Item deleted successfully!", "success")
    return redirect(url_for('facebook'))


# Route for Adding New Account
@app.route('/add_gmail_account', methods=['POST'])
def add_gmail_account():
    # name = request.form['name']
    # gmail = request.form['gmail']
    # password = request.form['password']
    # verified = request.form['verified']
    # created_date = datetime.strptime(request.form['created_date'], '%Y-%m-%d')
    # status = request.form['status']
    # description = request.form.get('description')
    #
    # new_account = GmailAccount(name=name, gmail=gmail, password=password, verified=verified,
    #                            created_date=created_date, status=status,
    #                            description=description)
    # db.session.add(new_account)
    # db.session.commit()

    return redirect(url_for('gmail'))


@app.route('/instagram')
# @app.route('/instagram/page/<int:page>')
# @app.route('/page')
def instagram(page=1):
    # per_page = 10  # Number of items per page
    # pagination = GmailAccount.query.paginate(page=page, per_page=per_page, error_out=False)
    #
    # if page > pagination.pages or page < 1:
    #     flash('Invalid page number', 'error')
    #     return redirect(url_for('gmail'))
    #
    # return render_template('gmail.html', items=pagination.items, pagination=pagination)
    return render_template('instagram.html')


@app.route('/threads')
# @app.route('/instagram/page/<int:page>')
# @app.route('/page')
def threads(page=1):
    # per_page = 10  # Number of items per page
    # pagination = GmailAccount.query.paginate(page=page, per_page=per_page, error_out=False)
    #
    # if page > pagination.pages or page < 1:
    #     flash('Invalid page number', 'error')
    #     return redirect(url_for('gmail'))
    #
    # return render_template('gmail.html', items=pagination.items, pagination=pagination)
    return render_template('threads.html')


@app.route('/tiktok')
# @app.route('/instagram/page/<int:page>')
# @app.route('/page')
def tiktok(page=1):
    # per_page = 10  # Number of items per page
    # pagination = GmailAccount.query.paginate(page=page, per_page=per_page, error_out=False)
    #
    # if page > pagination.pages or page < 1:
    #     flash('Invalid page number', 'error')
    #     return redirect(url_for('gmail'))
    #
    # return render_template('gmail.html', items=pagination.items, pagination=pagination)
    return render_template('tiktok.html')


@app.route('/youtube')
# @app.route('/instagram/page/<int:page>')
# @app.route('/page')
def youtube(page=1):
    # per_page = 10  # Number of items per page
    # pagination = GmailAccount.query.paginate(page=page, per_page=per_page, error_out=False)
    #
    # if page > pagination.pages or page < 1:
    #     flash('Invalid page number', 'error')
    #     return redirect(url_for('gmail'))
    #
    # return render_template('gmail.html', items=pagination.items, pagination=pagination)
    return render_template('youtube.html')


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/content')
@app.route('/content/page/<int:page>')
def content(page=1):
    files = get_files_and_folders(BASE_FOLDER_PATH)
    files.pop(0)
    # per_page = 10  # Number of items per page
    # pagination = None
    # pages = 0
    # if page > pagination.pages or page < 1:
    #     flash('Invalid page number', 'error')
    #     return redirect(url_for('content'))

    return render_template('content.html', files=files)


@app.route('/filter', methods=['POST'])
def filter_files():
    folder_name = request.form.get('folderName')
    search_keyword = request.form.get('keyword')

    # Apply filters based on user input
    files = get_files_and_folders(BASE_FOLDER_PATH, folder_name, search_keyword)

    return render_template('content.html', files=files)


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
        ydl.download(video_links)

    return jsonify({'message': 'Download started, check server for output'})


@app.route('/editor')
def editor(page=1):
    return render_template('editor.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login_account', methods=['POST'])
def login_account():
    return render_template('index.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()  # Ensure the database tables are created inside the application context
    app.run(debug=True, host='0.0.0.0')
