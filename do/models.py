from do import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(120), unique=True, nullable=False)
    goal = db.relationship('Goal', backref='owner', lazy=True)
    def __repr__(self):
        return f"{self.phone_number}"

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal_type = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(480))
    start_date = db.Column(db.Date)
    active = db.Column(db.Boolean, nullable=False, default=False)
    count = db.Column(db.Integer, nullable=False, default=0)
    streak = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    history = db.relationship('History', backref='goal', lazy=True)
    def __repr__(self):
        return f"{self.description}"

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    achieved = db.Column(db.Boolean)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=False)
    def __repr__(self):
        return f"{self.date}: {self.achieved}"
