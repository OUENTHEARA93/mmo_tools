from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from flask_sqlalchemy.pagination import Pagination
from flask_migrate import Migrate

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default_fallback_key')

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Define Account Model
class FacebookAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(100), nullable=False)
    page_name = db.Column(db.String(100), nullable=False)
    followers = db.Column(db.Integer, nullable=False)
    reached = db.Column(db.Integer, nullable=False)
    page_url = db.Column(db.String(200), nullable=False)
    created_date = db.Column(db.Date, nullable=False)
    monetization = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Account {self.account}>"


# Define Account Model
class GmailAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gmail = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    verified = db.Column(db.String(100), nullable=False)
    created_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Gmail {self.name}>"


# Define Account Model
class InstagramAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(100), nullable=False)
    gmail = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    followers = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.Date, nullable=False)
    monetization = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Gmail {self.name}>"


# Define TikTok Account Model
class TikTokAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(100), nullable=False)
    gmail = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    followers = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.Date, nullable=False)
    monetization = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Gmail {self.name}>"


@app.route('/')
def index():
    return render_template('index.html')


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


@app.route('/facebook')
@app.route('/facebook/page/<int:page>')
# @app.route('/page')
def facebook(page=1):
    per_page = 10  # Number of items per page
    pagination = FacebookAccount.query.paginate(page=page, per_page=per_page, error_out=False)

    print(pagination.items)
    if page > pagination.pages or page < 1:
        flash('Invalid page number', 'error')
        return redirect(url_for('facebook'))

    return render_template('facebook.html', items=pagination.items, pagination=pagination)


# Route for Adding New Account
@app.route('/add_account', methods=['POST'])
def add_account():
    account = request.form['account']
    page_name = request.form['page_name']
    followers = request.form['followers']
    reached = request.form['reached']
    page_url = request.form['page_url']
    created_date = datetime.strptime(request.form['created_date'], '%Y-%m-%d')
    monetization = request.form['monetization']
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


# GMAIL MANAGEMENT
@app.route('/gmail')
# @app.route('/gmail/page/<int:page>')
# @app.route('/page')
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


# @app.route('/gmail')
# @app.route('/gmail/<int:page>')
# def gmail(page=1):
#     per_page = 10  # Number of items per page
#     pagination = GmailAccount.query.paginate(page=page, per_page=per_page, error_out=False)
#
#     if page > pagination.pages or page < 1:
#         flash('Invalid page number', 'error')
#         return redirect(url_for('gmail'))
#
#     return render_template('gmail.html', items=pagination.items, pagination=pagination)


# Route for Adding New Account
@app.route('/add_gmail_account', methods=['POST'])
def add_gmail_account():
    name = request.form['name']
    gmail = request.form['gmail']
    password = request.form['password']
    verified = request.form['verified']
    created_date = datetime.strptime(request.form['created_date'], '%Y-%m-%d')
    status = request.form['status']
    description = request.form.get('description')

    new_account = GmailAccount(name=name, gmail=gmail, password=password, verified=verified,
                               created_date=created_date, status=status,
                               description=description)
    db.session.add(new_account)
    db.session.commit()

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


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure the database tables are created inside the application context
    app.run(debug=True)
