from candidate_analysis.framework.db import db

class Candidate(db.Model):
    __tablename__ = 'candidates'
    candidate_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80))
    skill = db.Column(db.Integer)
    experience = db.Column(db.String(80))
    salary = db.Column(db.Float)
    notice_period = db.Column(db.String(80))
    source = db.Column(db.Text)
    location_current = db.Column(db.Text)
    location_prefferred = db.Column(db.Text)
    open = db.Column(db.Boolean)
    wfh = db.Column(db.Boolean)
    company = db.Column(db.Text)
    company_website = db.Column(db.Text)
    date_added = db.Column(db.Integer)
    date_added_year = db.Column(db.Integer)
    date_added_month = db.Column(db.Integer)

    candidate_documents = db.relationship('CandidateDocument', backref='Candidate', lazy=True)

    def __repr__(self):
        return '<Candidate %r>' % self.candidate_id
