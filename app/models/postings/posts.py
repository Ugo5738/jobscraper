from datetime import datetime

from app.extensions import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website_name = db.Column(db.String(100))
    job_title = db.Column(db.String(100))
    job_company_name = db.Column(db.String(100))
    logo_url = db.Column(db.String(100))
    job_description = db.Column(db.String(20000))
    location = db.Column(db.String(100))
    category = db.Column(db.String(100))
    salary_range = db.Column(db.String(100))
    post_time = db.Column(db.String(100))
    fill_date = db.Column(db.String(100), default=datetime.utcnow().strftime("%Y-%m-%d"))

    # define the one-to-many relationship
    job_tags = db.relationship("JobTag", backref="post", lazy=True)

    def __repr__(self):
        return f"<Website: {self.website_name}>"


class JobTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(100))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    def __repr__(self):
        return f"<JobTag: {self.tag_name}>"
