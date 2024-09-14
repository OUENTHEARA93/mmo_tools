import logging

import yt_dlp
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from flask_sqlalchemy.pagination import Pagination
from flask_migrate import Migrate

from models import db, FacebookAccount

app = Flask(__name__)

# Configure database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

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

    return render_template('facebook.html', items=pagination.items, pagination=pagination)


# Route for Adding New Account
# @app.route('/add_account', methods=['POST'])
# def add_account():
#     account = request.form['account']
#     page_name = request.form['page_name']
#     followers = request.form['followers']
#     reached = request.form['reached']
#     # page_url = request.form['page_url']
#     created_date = datetime.strptime(request.form['created_date'], '%Y-%m-%d')
#     monetization = request.form['monetization']
#     description = request.form.get('description')
#
#     new_account = FacebookAccount(account=account, page_name=page_name, followers=followers,
#                                   reached=reached, created_date=created_date,
#                                   monetization=monetization, description=description)
#     db.session.add(new_account)
#     db.session.commit()
#
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
    return render_template("view_item.html", item=account)


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
#     return render_template('facebook.html', items=items)


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
# @app.route('/instagram/page/<int:page>')
# @app.route('/page')
def content(page=1):
    return render_template('content.html')


@app.route('/download', methods=['POST'])
def download():
    save_as = request.form.get('save_as')
    video_size = request.form.get('video_size')
    folder_name = request.form.get('folder_name')
    video_links = request.form.get('video_links').strip().split('\n')

    download_path = os.path.join('downloads', folder_name)
    os.makedirs(download_path, exist_ok=True)

    # Configure yt-dlp options based on user input
    ydl_opts = {
        'format': f'bestvideo[height<={video_size}]+bestaudio/best[height<={video_size}]',
        'outtmpl': os.path.join(download_path, f'%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3' if save_as == 'MP3' else 'mp4',
        }] if save_as == 'MP3' else None
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_links)

    # Here you might want to return something more meaningful, like a success message or link to the downloaded files
    return jsonify({'message': 'Download started, check server for output'})


@app.route('/editor')
# @app.route('/instagram/page/<int:page>')
# @app.route('/page')
def editor(page=1):
    return render_template('editor.html')


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()  # Ensure the database tables are created inside the application context
    app.run(debug=True, host='0.0.0.0')
