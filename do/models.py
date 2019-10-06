from do import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(120), unique=True, nullable=False)
    goal = db.relationship('Goal', backref='owner', lazy=True)
    def __repr__(self):
        return f"{self.phone_number}"

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(480), nullable=False)
    goal_type = db.Column(db.String(30), nullable=False)
    # achieved_tally = db.Column(db.Integer)
    # streak = db.Column(db.Integer)
    # longest_streak
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"{self.description}"
