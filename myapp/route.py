import datetime
import os

import pyotp
import yt_dlp
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from myapp import app, BASE_FOLDER_PATH
from myapp import db
from myapp.models import Account, Page, Group, Monetization, Earning
from myapp.utils import get_files_and_folders, fetch_video_info


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


@app.route('/facebook/page')
@app.route('/facebook/page/<int:page>')
def facebook_page(page=1):
    per_page = 10  # Number of items per page
    pagination = Page.query.order_by(Page.followers_count.desc()).paginate(page=page, per_page=per_page,
                                                                           error_out=False)
    for item in pagination.items:
        print(item)

    if page > pagination.pages or page < 1:
        flash('Invalid page number', 'error')
        return redirect(url_for('facebook'))
    return render_template('/facebook/pages.html', items=pagination.items, pagination=pagination)
    # return render_template('/facebook/pages.html', items=pagination)


# View Item
@app.route("/view/<int:id>")
def view_item(id):
    account = Account.query.get_or_404(id)
    return render_template("/facebook/view_page.html", item=account)


@app.route('/facebook/accounts/add', methods=['GET', 'POST'])
def add_facebook_account():
    return render_template('/facebook/add_accounts.html')


@app.route('/facebook/accounts/bulk_add', methods=['GET', 'POST'])
def bulk_add_facebook_account():
    if request.method == 'POST':
        data = request.form.get('bulk_data')  # Get bulk data from form

        if not data:
            flash("No data provided", "error")
            return redirect(url_for('bulk_add_facebook_account'))

        # Split input into lines (each line is an account)
        lines = data.strip().split('\n')

        for line in lines:
            try:

                # Split by '|' and count fields
                fields = line.split('|')

                # Check if format is (uid|name|password|2fa)
                if len(fields) == 4:
                    uid, username, password, two_fa = fields
                    # Assign default or empty values to the missing fields
                    gender, dob, mail, pass_mail = None, None, None, None
                elif len(fields) == 8:
                    # Full format: (uid|name|password|2fa|gender|dob|mail|pass_mail)
                    uid, username, password, two_fa, gender, dob, mail, pass_mail = fields
                else:
                    flash(f"Invalid format for line: {line}", "error")
                    continue

                # Create Account object
                account = Account(
                    uid=uid,
                    username=username,
                    password=password,
                    gender=gender,
                    dob=dob,
                    mail=mail,
                    pass_mail=pass_mail,
                    two_fa=two_fa

                )

                # Add to the session
                db.session.add(account)

            except Exception as e:
                flash(f"Error processing line: {line}. Error: {str(e)}", "error")
                continue

        # Commit all the changes
        db.session.commit()
        flash("Accounts added successfully", category="success")
    return render_template('/facebook/add_bulk_accounts.html')


@app.route('/facebook/accounts/delete/<int:id>', methods=['POST'])
def facebook_delete_account(id):
    account = Account.query.get_or_404(id)

    try:
        db.session.delete(account)
        db.session.commit()
        flash("Account deleted successfully", category="success")
        return redirect(url_for('facebook_accounts'))
    except Exception as e:
        flash(f"Error deleting account: {str(e)}", category="error")


@app.route("/facebook/addpage")
# @app.route('/facebook')
@app.route('/facebook/addpage/page/<int:page>')
def load_create_page(page=1):
    per_page = 10  # Number of items per page
    # pagination = Account.query.order_by(Account.followers.desc()).paginate(page=page, per_page=per_page,
    #                                                                                        error_out=False)
    #
    # if page > pagination.pages or page < 1:
    #     flash('Invalid page number', 'error')
    #     return redirect(url_for('facebook'))

    return render_template('/facebook/add_pages.html')  # , items=pagination.items, pagination=pagination)


@app.route('/facebook/add/page', methods=['POST'])
def add_page():
    account = request.form.get('account')
    page_name = request.form.get('page_name')
    followers = request.form.get('followers')
    reached = request.form.get('reached')
    page_url = request.form.get('page_url')
    created_date = request.form.get('created_date')
    monetization = request.form.get('monetization')
    description = request.form.get('description')

    # new_account = FacebookAccount(account=account, page_name=page_name, followers=followers,
    #                               reached=reached, page_url=page_url, created_date=created_date,
    #                               monetization=monetization, description=description)
    # db.session.add(new_account)
    # db.session.commit()
    return redirect(url_for('load_create_page'))


# Edit Item
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_item(id):
    # item = FacebookAccount.query.get_or_404(id)
    # if request.method == "POST":
    #     item.account = request.form['account']
    #     item.page_name = request.form['page_name']
    #
    #     item.followers = request.form['followers']
    #     item.reached = request.form['reached']
    #     item.created_date = datetime.strptime(request.form['created_date'], '%Y-%m-%d')
    #     item.monetization = request.form['monetization']
    #     item.description = request.form['description']
    #     # update other fields similarly
    #     db.session.commit()
    #     flash("Item updated successfully!", "success")
    #     return redirect(url_for('facebook'))  # Redirect to the main page after editing

    return render_template("/facebook/edit_page_item.html")  # , item=item)


# Delete Item
@app.route("/facebook/addpage/delete/<int:id>", methods=["POST"])
def delete_item(id):
    # item = FacebookAccount.query.get_or_404(id)
    # db.session.delete(item)
    # db.session.commit()
    # flash("Item deleted successfully!", "success")
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
@app.route('/facebook/accounts/<int:page>')
def facebook_accounts(page=1):
    devices = [
        {'id': 1, 'udid': 'emululator-3272', 'name': 'Samsung S20', 'status': 'live'},
        {'id': 2, 'udid': 'emululator-3472', 'name': 'Samsung S10', 'status': 'live'},
        {'id': 3, 'udid': 'emululator-3273', 'name': 'Samsung S7', 'status': 'live'},
        {'id': 4, 'udid': 'emululator-3172', 'name': 'Samsung S8', 'status': 'live'}
    ]
    per_page = 10  # Number of items per page
    pagination = Account.query.order_by(Account.id.desc()).paginate(page=page, per_page=per_page,
                                                                    error_out=False)
    if page > pagination.pages or page < 1:
        flash('Invalid page number', 'error')
        return redirect(url_for('facebook'))
    return render_template('/facebook/accounts.html', items=pagination.items, pagination=pagination, devices=devices)
    # return render_template('/facebook/accounts.html')


@app.route('/facebook/groups')
def facebook_groups(page=1):
    per_page = 10  # Number of items per page
    pagination = Group.query.order_by(Group.id.desc()).paginate(page=page, per_page=per_page,
                                                                error_out=False)
    # for item in pagination.items:
    #     print(item)
    #
    # if page > pagination.pages or page < 1:
    #     flash('Invalid page number', 'error')
    #     return redirect(url_for('facebook'))
    return render_template('/facebook/groups.html')  # , items=pagination.items, pagination=pagination)


@app.route('/facebook/monetize')
def facebook_monetize(page=1):
    # per_page = 10  # Number of items per page
    # pagination = Monetization.query.order_by(Monetization.id.desc()).paginate(page=page, per_page=per_page,
    #                                                                           error_out=False)
    # for item in pagination.items:
    #     print(item)
    #
    # if page > pagination.pages or page < 1:
    #     flash('Invalid page number', 'error')
    #     return redirect(url_for('facebook'))
    return render_template('/facebook/monetization.html')  # , items=pagination.items, pagination=pagination)


@app.route('/facebook/earning')
def facebook_earning(page=1):
    per_page = 10  # Number of items per page
    pagination = Earning.query.order_by(Earning.id.desc()).paginate(page=page, per_page=per_page,
                                                                    error_out=False)
    # for item in pagination.items:
    #     print(item)
    #
    # if page > pagination.pages or page < 1:
    #     flash('Invalid page number', 'error')
    #     return redirect(url_for('facebook'))
    return render_template('/facebook/earning.html')  # , items=pagination.items, pagination=pagination)


@app.route('/facebook/post')
def facebook_reels():
    return render_template('/facebook/post.html')


@app.route('/telegram/channel')
def telegram_channels():
    return render_template('/telegram/channels.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/tools/security', methods=['GET', 'POST'])
def security_tools():
    return render_template('/tools/security_2fa.html')


@app.route('/security/generate_code', methods=['POST'])
def generate_code():
    data = request.get_json()
    fa_key = data.get('fa_key').replace(" ", "")

    if not fa_key:
        return jsonify({'error': 'Invalid 2FA key'}), 400

    try:
        # Create a TOTP object and generate the current TOTP code
        totp = pyotp.TOTP(fa_key)
        code = totp.now()  # Get the current code
        print(code)
        return jsonify({'code': code})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/scrape_videos', methods=['POST'])
def scrape_videos():
    video_links = request.json.get('video_links')
    video_data = []

    for link in video_links:
        video_info = fetch_video_info(link)
        video_data.append(video_info)

    return jsonify(video_data)
