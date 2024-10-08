import datetime
import os
import subprocess

import pyotp
import yt_dlp
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from myapp import app, BASE_FOLDER_PATH
from myapp import db
from myapp.models import Account, Page, Group, Monetization, Earning, Bank, Gmail, Website, Youtube, Tiktok, Device, \
    Instagram, Telegram
from myapp.utils import get_files_and_folders, fetch_video_info, format_file_size
import pandas as pd
from adbutils import adb


@app.route('/')
def index():
    return render_template('index.html')


@app.before_request
def create_tables():
    db.create_all()


def get_connected_devices():
    # Run adb command to list devices
    result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # Split the output into lines
    devices = result.stdout.splitlines()
    # Extract device IDs
    connected_devices = [line.split()[0] for line in devices[1:] if line.strip() and "device" in line]
    return connected_devices


def get_device_info(device_id):
    # Run adb command to get device information
    result = subprocess.run(["adb", "-s", device_id, "shell", "getprop"], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)
    return result.stdout


@app.route('/check_device')
@app.route('/check_device/page/<int:page>')
def check_device(page=1):
    # devices_df = get_devices()
    # Get the list of connected devices
    # devices = get_connected_devices()

    # if devices:
    #     print(f"Connected devices: {devices}")
    #     for device in devices:
    #         print(f"\nDevice ID: {device}")
    #         # Get and print detailed device information
    #         device_info = get_device_info(device)
    #         print(device_info)
    # else:
    #     print("No devices connected.")
    # print(devices)

    per_page = 10  # Number of items per page
    pagination = Device.query.order_by(Device.id.desc()).paginate(page=page, per_page=per_page,
                                                                  error_out=False)
    # print("checking...device")
    if page > pagination.pages or page < 1:
        flash('Invalid page number', 'error')
        return redirect(url_for('check_device'))
    return render_template('/device/devices.html', items=pagination.items, pagination=pagination)


# GMAIL MANAGEMENT
@app.route('/gmail')
def gmail(page=1):
    return render_template('/gmail/accounts.html')


@app.route('/gmail/register')
def gmail_register(page=1):
    return render_template('/gmail/gmail_register.html')


@app.route('/website')
def website(page=1):
    return render_template('/website/page.html')


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
                print(fields)
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


# @app.route("/facebook/addpage")
# # @app.route('/facebook')
# @app.route('/facebook/addpage/page/<int:page>')
# def load_create_page(page=1):
#     per_page = 10  # Number of items per page
#     # pagination = Account.query.order_by(Account.followers.desc()).paginate(page=page, per_page=per_page,
#     #                                                                                        error_out=False)
#     #
#     # if page > pagination.pages or page < 1:
#     #     flash('Invalid page number', 'error')
#     #     return redirect(url_for('facebook'))
#
#     return render_template('/facebook/add_pages.html')  # , items=pagination.items, pagination=pagination)


# @app.route('/facebook/add/page', methods=['POST'])
# def add_page():
#     account = request.form.get('account')
#     page_name = request.form.get('page_name')
#     followers = request.form.get('followers')
#     reached = request.form.get('reached')
#     page_url = request.form.get('page_url')
#     created_date = request.form.get('created_date')
#     monetization = request.form.get('monetization')
#     description = request.form.get('description')
#
#     # new_account = FacebookAccount(account=account, page_name=page_name, followers=followers,
#     #                               reached=reached, page_url=page_url, created_date=created_date,
#     #                               monetization=monetization, description=description)
#     # db.session.add(new_account)
#     # db.session.commit()
#     return redirect(url_for('load_create_page'))


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
@app.route('/instagram/page/<int:page>')
def instagram(page=1):
    per_page = 10
    pagination = Instagram.query.order_by(Instagram.id.desc()).paginate(page=page, per_page=per_page,
                                                                        error_out=False)
    if page > pagination.pages or page < 1:
        flash('Invalid page number', 'error')
        return redirect(url_for('instagram'))
    return render_template('/instagram/accounts.html', items=pagination.items, pagination=pagination)
    # return render_template('/instagram/accounts.html')


@app.route('/threads')
def threads(page=1):
    return render_template('/threads/accounts.html')


@app.route('/tiktok')
@app.route('/tiktok/page/<int:page>')
def tiktok(page=1):
    per_page = 10  # Number of items per page
    pagination = Tiktok.query.order_by(Tiktok.id.desc()).paginate(page=page, per_page=per_page,
                                                                  error_out=False)

    if page > pagination.pages or page < 1:
        flash('Invalid page number', 'error')
        return redirect(url_for('tiktok'))
    return render_template('/tiktok/account.html', items=pagination.items, pagination=pagination)


@app.route('/youtube')
@app.route('/youtube/page/<int:page>')
def youtube(page=1):
    per_page = 10  # Number of items per page
    pagination = Youtube.query.order_by(Youtube.subscriber.desc()).paginate(page=page, per_page=per_page,
                                                                            error_out=False)

    if page > pagination.pages or page < 1:
        flash('Invalid page number', 'error')
        return redirect(url_for('youtube'))
    return render_template('/youtube/channels.html', items=pagination.items, pagination=pagination)


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


# @app.route('/download', methods=['POST'])
# def download():
#     save_as = request.form.get('savefile')
#     video_size = request.form.get('video_size')
#     folder_name = request.form.get('folderName')
#     video_links = request.form.get('videoLinks').strip().split('\n')
#
#     download_path = os.path.join('downloads', folder_name)
#     os.makedirs(download_path, exist_ok=True)
#
#     # Configure yt-dlp options based on user input
#     ydl_opts = {
#         'format': f'bestvideo[height<={video_size}]+bestaudio/best[height<={video_size}]',
#         'outtmpl': os.path.join(download_path, f'%(title)s.%(ext)s'),
#         'retries': 10,
#         'socket_timeout': 30,
#         'noprogress': True,  # Disable progress reporting
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3' if save_as == 'MP3' else 'mp4',
#         }] if save_as == 'MP3' else []  # Ensure postprocessors is an empty list if not 'MP3'
#     }
#
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         try:
#             ydl.download(video_links)
#         except yt_dlp.utils.DownloadError as e:
#             print(f"Skipping video {video_links} due to error: {e}")
#
#     return jsonify({'message': 'Download started, check server for output'})
# Function to get available formats and metadata using yt-dlp
# def get_video_formats(video_link):
#     ydl_opts = {"quiet": True, "no_warnings": True, "format": "all"}
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info_dict = ydl.extract_info(video_link, download=False)
#         formats = info_dict.get('formats', [])
#         # Filter out audio-only formats
#         video_formats = [fmt for fmt in formats if fmt.get('vcodec') != 'none']
#         return {
#             "folderName": info_dict.get("title"),
#             "title": info_dict.get("title"),
#             "size": round(info_dict.get("filesize", 0) / (1024 * 1024), 2) if info_dict.get("filesize") else "Unknown",
#             "duration": f"{info_dict.get('duration') // 60} min {info_dict.get('duration') % 60} sec",
#             "views": info_dict.get("view_count", 0),
#             "description": info_dict.get("description", "No description available."),
#             "formats": [{"format_id": fmt["format_id"], "resolution": fmt["resolution"], "ext": fmt["ext"],
#                          "filesize": round(fmt.get("filesize", 0) / (1024 * 1024), 2) if fmt.get(
#                              "filesize") else "Unknown"}
#                         for fmt in video_formats]
#         }


# Function to download the video based on the selected format
# def download_video(video_link, format_id):
#     ydl_opts = {
#         "format": format_id,
#         "outtmpl": os.path.join("downloads", "%(title)s.%(ext)s"),  # Download to the 'downloads' folder
#         "quiet": True,
#         "no_warnings": True,
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([video_link])
#     return {"status": "success", "message": f"Downloaded video: {video_link}"}


@app.route('/editor')
def editor(page=1):
    return render_template('/content/editor.html')


@app.route('/facebook/accounts')
@app.route('/facebook/accounts/<int:page>')
def facebook_accounts(page=1):
    # devices = [
    #     {'id': 1, 'udid': 'emululator-3272', 'name': 'Samsung S20', 'status': 'live'},
    #     {'id': 2, 'udid': 'emululator-3472', 'name': 'Samsung S10', 'status': 'live'},
    #     {'id': 3, 'udid': 'emululator-3273', 'name': 'Samsung S7', 'status': 'live'},
    #     {'id': 4, 'udid': 'emululator-3172', 'name': 'Samsung S8', 'status': 'live'}
    # ]
    per_page = 10  # Number of items per page
    pagination = Account.query.order_by(Account.id.desc()).paginate(page=page, per_page=per_page,
                                                                    error_out=False)
    if page > pagination.pages or page < 1:
        flash('Invalid page number', 'error')
        return redirect(url_for('facebook'))
    return render_template('/facebook/accounts.html', items=pagination.items, pagination=pagination)
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


@app.route('/bank/list')
def bank_list(page=1):
    per_page = 10  # Number of items per page
    pagination = Bank.query.order_by(Bank.id.desc()).paginate(page=page, per_page=per_page,
                                                              error_out=False)

    if page > pagination.pages or page < 1:
        flash('Invalid page number', 'error')
        return redirect(url_for('bank_list'))
    return render_template('/banks/bank_list.html', items=pagination.items, pagination=pagination)


# *********************************************
#   GMAIL MANAGEMENT
# *********************************************
@app.route('/add_gmail', methods=['POST'])
def add_gmail():
    data = request.get_json()

    # Extract data from the form
    new_mail = Gmail(
        name=data['name'],
        gmail=data['gmail'],
        password=data['password'],
        verify=data['verify'],
        status=data['status'],
        description=data['description']
    )

    db.session.add(new_mail)
    db.session.commit()

    return jsonify({'message': 'Gmail added successfully!'})


@app.route('/gmail/list')
def gmail_list(page=1):
    per_page = 10  # Number of items per page
    pagination = Gmail.query.order_by(Gmail.id.desc()).paginate(page=page, per_page=per_page,
                                                                error_out=False)

    if page > pagination.pages or page < 1:
        flash('Invalid page number', 'error')
        return redirect(url_for('gmail_list'))
    return render_template('/gmail/accounts.html', items=pagination.items, pagination=pagination)


@app.route('/add_bank', methods=['POST'])
def add_bank():
    data = request.get_json()

    # Extract data from the form
    new_bank = Bank(
        bank_name=data['bank_name'],
        account_number=data['account_number'],
        account_name=data['account_name'],
        swift_code=data['swift_code'],
        routing_number=data['routing_number'],
        gmail=data['gmail'],
        status=data['status'],
        description=data['description']
    )

    db.session.add(new_bank)
    db.session.commit()

    return jsonify({'message': 'Bank added successfully!'})


@app.route('/website/list')
def website_list(page=1):
    per_page = 10  # Number of items per page
    pagination = Website.query.order_by(Website.id.desc()).paginate(page=page, per_page=per_page,
                                                                    error_out=False)

    if page > pagination.pages or page < 1:
        flash('Invalid page number', 'error')
        return redirect(url_for('website_list'))
    return render_template('/website/page.html', items=pagination.items, pagination=pagination)


@app.route('/add_website', methods=['POST'])
def add_website():
    data = request.get_json()

    # Extract data from the form
    new_website = Website(
        domain=data['domain'],
        hosting=data['hosting'],
        gmail=data['gmail'],
        password=data['password'],
        link=data['link'],
        adsnetwork=data['adsnetwork'],
        earning=data['earning'],
        status=data['status'],
        description=data['description']
    )

    db.session.add(new_website)
    db.session.commit()

    return jsonify({'message': 'Website added successfully!'})


@app.route('/bank/earning')
def earning(page=1):
    per_page = 10  # Number of items per page
    pagination = Earning.query.order_by(Earning.id.desc()).paginate(page=page, per_page=per_page,
                                                                    error_out=False)
    # for item in pagination.items:
    #     print(item)
    #
    # if page > pagination.pages or page < 1:
    #     flash('Invalid page number', 'error')
    #     return redirect(url_for('facebook'))
    return render_template('/banks/earning.html', items=pagination.items, pagination=pagination)


@app.route('/facebook/post')
def facebook_reels():
    return render_template('/facebook/post.html')


@app.route('/telegram/channel')
@app.route('/telegram/channel/page/<int:page>')
def telegram_accounts(page=1):
    per_page = 10

    pagination = Telegram.query.order_by(Telegram.id.desc()).paginate(page=page, per_page=per_page,
                                                                      error_out=False)
    # for item in pagination.items:
    #     print(item)
    #
    if page > pagination.pages or page < 1:
        flash('Invalid page number', 'error')
        return redirect(url_for('telegram_accounts'))
    return render_template('/telegram/account.html', items=pagination.items, pagination=pagination)


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


# Mocking device list for demonstration purposes
# def get_devices():
#     devices = adb.device_list()
#     device_info = []
#     for idx, device in enumerate(devices):
#         device_info.append({
#             "No": idx + 1,
#             "Name": device.serial,
#             "OS Version": device.prop.model,
#             "App Installed": "Yes" if "com.facebook.katana" in device.list_packages() else "No",
#             "Category": "Phone" if "device" in device.serial else "Emulator",
#             "Status": "Active",
#             "Description": "Connected"
#         })
#     return pd.DataFrame(device_info)
#
#
# @app.route("/check_device", methods=["GET"])
# def check_device():
#     # Return updated device list
#     devices_df = get_devices()
#     return jsonify(devices_df.to_dict(orient="records"))


# @app.route('/scrape_videos', methods=['POST'])
# def scrape_videos():
#     video_url = request.json.get('video_links')
#     if not video_url:
#         return jsonify({'error': 'No URL provided'}), 400
#
#     try:
#         ydl_opts = {'quiet': True}
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info_dict = ydl.extract_info(video_url, download=False)
#         # print(info_dict.get('filesize', 0))
#         return jsonify({
#             'title': info_dict.get('title', ''),
#             'duration': info_dict.get('duration_string', 0),
#             'resolution': info_dict.get('resolution', 0),
#             'views': info_dict.get('view_count', 0),
#             'size': info_dict.get('filesize', 0),
#             'description': info_dict.get('description', '')
#         })
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# Set the download directory
DOWNLOAD_DIR = './downloads'

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)


# Route to scrape video info
@app.route('/scrape_video_info', methods=['POST'])
def scrape_video_info():
    # data = request.get_json()
    # video_url = data.get('url')
    #
    # ydl_opts = {
    #     'quiet': True,
    #     'skip_download': True,  # Only retrieve metadata
    # }
    #
    # try:
    #     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #         info = ydl.extract_info(video_url, download=False)
    #         return jsonify({
    #             'title': info.get('title', 'Unknown Title'),
    #             'duration': info.get('duration', 0)
    #         })
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500
    video_url = request.json.get('url')
    # print(f"SCRAPE: {video_url}")
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
        # print(info_dict)
        return jsonify({
            'title': info_dict.get('title', ''),
            'duration': info_dict.get('duration_string', 0),
            'resolution': info_dict.get('resolution', 0),
            'views': info_dict.get('view_count', 0),
            'size': format_file_size(info_dict.get("filesize")),#info_dict.get('filesize', 0),
            'description': info_dict.get('description', '')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Download video function
def download_video(video_url, title):
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_DIR, f'{title}.mp4'),
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return True
    except Exception as e:
        print(f"Error downloading {title}: {str(e)}")
        return False


@app.route('/download', methods=['POST'])
def download():
    data = request.json
    video_url = data.get('video_url')
    title = data.get('title')

    if not video_url or not title:
        return jsonify({'status': 'error', 'message': 'Missing video URL or title'}), 400

    success = download_video(video_url, title)

    if success:
        return jsonify({'status': 'success', 'message': f'{title} downloaded successfully!'})
    else:
        return jsonify({'status': 'error', 'message': f'Failed to download {title}'}), 500

# Route to download video
# @app.route('/download_video', methods=['POST'])
# def download_video():
#     data = request.get_json()
#     video_url = data.get('url')
#
#     ydl_opts = {
#         'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
#         'format': 'best',
#     }
#     print(f"START-DOWNLOAD {video_url}")
#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([video_url])
#         return jsonify({'success': True})
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500
