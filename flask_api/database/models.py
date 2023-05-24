from flask_api import db

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    student_password = db.Column(db.String(120), nullable=False)
    gCredentials = db.Column(db.String(120))
    moodle_data = db.relationship('MoodleData', backref='user')

    def __repr__(self):
        return f'<User {self.user_id}>'
    
class MoodleData(db.Model):
    __tablename__ = 'moodle_data'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    assessment_name = db.Column(db.String(255))
    assessment_due_date = db.Column(db.Date)
    assessment_due_time = db.Column(db.Time)
    assessment_detail = db.Column(db.Text)
    assessment_url = db.Column(db.String(255))

    def __repr__(self):
        return f'<MoodleData {self.assessment_name}>'