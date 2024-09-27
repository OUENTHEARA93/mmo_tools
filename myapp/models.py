from datetime import datetime
from myapp import db


# class FacebookAccount(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     account = db.Column(db.String(100))
#     page_name = db.Column(db.String(100))
#     followers = db.Column(db.Integer)
#     reached = db.Column(db.Integer)
#     page_url = db.Column(db.String(200))
#     created_date = db.Column(db.String(50))
#     monetization = db.Column(db.String(20))
#     description = db.Column(db.Text)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Device name
    type = db.Column(db.String(50), nullable=False)  # 'Phone' or 'LDPlayer'
    os_version = db.Column(db.String(50), nullable=True)  # OS version
    status = db.Column(db.String(50), nullable=False, default="active")  # Active, inactive
    last_login = db.Column(db.DateTime, nullable=True)  # Last login time for this device
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Device {self.name}>"


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(100), unique=True, nullable=False)  # Facebook UID
    username = db.Column(db.String(100), nullable=False)  # Username or email
    password = db.Column(db.String(100), nullable=False)  # Password
    gender = db.Column(db.String(10), nullable=False)  # Gender
    dob = db.Column(db.DateTime, nullable=False)  # Date of Birth
    mail = db.Column(db.String(100), nullable=True)  # Email
    pass_mail = db.Column(db.String(100), nullable=True)  # Password email
    two_fa = db.Column(db.String(100), nullable=True)  # 2FA code
    access_token = db.Column(db.String(255), nullable=True)  # Store tokens for API access
    last_login = db.Column(db.DateTime, nullable=True)  # Last login timestamp
    status = db.Column(db.String(50), default="active")  # Active, inactive, banned, etc.
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))  # Associated device
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    device = db.relationship('Device', backref=db.backref('accounts', lazy=True))

    def __repr__(self):
        return f"<Account {self.username}>"


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.String(100), unique=True, nullable=False)  # Facebook Page ID
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))  # Associated Facebook account
    name = db.Column(db.String(100), nullable=False)  # Page name
    category = db.Column(db.String(100), nullable=True)  # Page category (business, personal, etc.)
    followers_count = db.Column(db.Integer, nullable=True)  # Number of followers
    reached = db.Column(db.Integer, nullable=True)
    monetization_enabled = db.Column(db.Boolean, default=False)  # Monetization status
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    account = db.relationship('Account', backref=db.backref('pages', lazy=True))

    def __repr__(self):
        return f"<Page {self.name}>"


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.String(100), unique=True, nullable=False)  # Facebook Group ID
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))  # Associated Facebook account
    name = db.Column(db.String(100), nullable=False)  # Group name
    members_count = db.Column(db.Integer, nullable=True)  # Number of members in the group
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    account = db.relationship('Account', backref=db.backref('groups', lazy=True))

    def __repr__(self):
        return f"<Group {self.name}>"


class Monetization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    status = db.Column(db.String(50), default="pending")  # Pending, approved, rejected
    monetization_type = db.Column(db.String(50), nullable=False)  # Ad Breaks, Fan Subscriptions, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    account = db.relationship('Account', backref=db.backref('monetization', lazy=True))
    page = db.relationship('Page', backref=db.backref('monetization', lazy=True))

    def __repr__(self):
        return f"<Monetization {self.page_id} - {self.monetization_type}>"


class Earning(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monetization_id = db.Column(db.Integer, db.ForeignKey('monetization.id'))
    amount = db.Column(db.Float, nullable=False)  # Earning amount
    currency = db.Column(db.String(10), nullable=False, default="USD")  # Currency of earnings
    payment_date = db.Column(db.DateTime, nullable=True)  # Payment release date
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    monetization = db.relationship('Monetization', backref=db.backref('earnings', lazy=True))

    def __repr__(self):
        return f"<Earning {self.amount} {self.currency}>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)  # Post content
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)
    scheduled_at = db.Column(db.DateTime, nullable=True)  # Schedule a post for future time
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    account = db.relationship('Account', backref=db.backref('posts', lazy=True))
    page = db.relationship('Page', backref=db.backref('posts', lazy=True))
    group = db.relationship('Group', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f"<Post {self.id}>"


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255), nullable=False)  # Action description (e.g., "Created Post", "Updated Page")
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))  # Account that performed the action
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # When the action occurred
    details = db.Column(db.Text, nullable=True)  # Optional additional details

    account = db.relationship('Account', backref=db.backref('logs', lazy=True))

    def __repr__(self):
        return f"<Log {self.action} by Account {self.account_id}>"


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))  # Recipient account
    message = db.Column(db.String(255), nullable=False)  # Notification message
    is_read = db.Column(db.Boolean, default=False)  # Status: Read/Unread
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # When the notification was created

    account = db.relationship('Account', backref=db.backref('notifications', lazy=True))

    def __repr__(self):
        return f"<Notification {self.message} to Account {self.account_id}>"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))  # Account responsible for the task
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))  # Post associated with the task
    scheduled_time = db.Column(db.DateTime, nullable=False)  # Time when the task should execute
    status = db.Column(db.String(50), nullable=False, default="pending")  # Pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    account = db.relationship('Account', backref=db.backref('tasks', lazy=True))
    post = db.relationship('Post', backref=db.backref('task', lazy=True))

    def __repr__(self):
        return f"<Task {self.id} for Post {self.post_id}>"


class Insight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(50), nullable=False)  # Could be 'Page', 'Group', or 'Post'
    entity_id = db.Column(db.Integer, nullable=False)  # ID of the Page, Group, or Post
    views = db.Column(db.Integer, nullable=False, default=0)  # Number of views
    engagements = db.Column(db.Integer, nullable=False, default=0)  # Likes, shares, etc.
    earnings = db.Column(db.Float, nullable=False, default=0.0)  # Earnings from this entity (if applicable)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Insight {self.entity_type} {self.entity_id}>"


class AdCampaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))  # Associated Facebook account
    name = db.Column(db.String(100), nullable=False)  # Campaign name
    budget = db.Column(db.Float, nullable=False)  # Campaign budget
    start_date = db.Column(db.DateTime, nullable=False)  # Start date of the campaign
    end_date = db.Column(db.DateTime, nullable=True)  # End date (optional)
    status = db.Column(db.String(50), nullable=False, default="active")  # Active, paused, completed, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    account = db.relationship('Account', backref=db.backref('ad_campaigns', lazy=True))

    def __repr__(self):
        return f"<AdCampaign {self.name}>"


class ApiKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), unique=True, nullable=False)  # API key
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))  # Associated account
    status = db.Column(db.String(50), default="active")  # Active, revoked
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    account = db.relationship('Account', backref=db.backref('api_keys', lazy=True))

    def __repr__(self):
        return f"<ApiKey {self.key}>"
