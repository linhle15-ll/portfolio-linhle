import os
from datetime import datetime
from flask import Flask, jsonify, render_template, request
from peewee import *
import datetime

from app.data import (
    profile,
    about_paragraphs,
    experiences,
    education,
    journal_entries,
)

app = Flask(__name__)

# DATABASE SETUP
database_name = os.getenv("MYSQL_DATABASE") or "timeline.db"
database_user = os.getenv("MYSQL_USER")
database_password = os.getenv("MYSQL_PASSWORD")
database_host = os.getenv("MYSQL_HOST") or "localhost"

if database_user and database_password:
    mydb = MySQLDatabase(
        database_name,
        user=database_user,
        password=database_password,
        host=database_host,
        port=3306
    )
else:
    mydb = SqliteDatabase("timeline.db")

print(f"MY DATABASE {mydb}")

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect(reuse_if_open=True)
mydb.create_tables([TimelinePost], safe=True)

# NAVIGATION
nav_links = [
    {"label": "Home", "href": "/"},
    {"label": "Experience", "href": "/experience"},
    {"label": "Journal", "href": "/journal"},
    {"label": "Timeline", "href": "/timeline"}
]


@app.context_processor
def inject_globals():
    """Makes these available in every template without passing explicitly."""
    return {
        "profile": profile,
        "nav_links": nav_links,
        "current_year": datetime.datetime.now().year,
    }


@app.route("/")
def home():
    return render_template(
        "index.html",
        about_paragraphs=about_paragraphs,
        education_info=education[0] if education else {},
    )


@app.route("/experience")
def experience():
    return render_template("experience.html", experiences=experiences)

@app.route("/journal")
def journal():
    return render_template("journal.html", gallery=journal_entries)

@app.route("/timeline")
def timeline():
    return render_template("timeline.html", title="timeline")

# DATABASE
@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    content = request.form.get('content', '').strip()

    if not name or not email or not content:
        return jsonify({'error': 'name, email, and content are required'}), 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return jsonify({
        'id': timeline_post.id,
        'name': timeline_post.name,
        'email': timeline_post.email,
        'content': timeline_post.content,
        'created_at': timeline_post.created_at.isoformat() if timeline_post.created_at else None,
    })


@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
    return jsonify({
        'timeline_posts': [
            {
                'id': post.id,
                'name': post.name,
                'email': post.email,
                'content': post.content,
                'created_at': post.created_at.isoformat() if post.created_at else None,
            }
            for post in posts
        ]
    })


@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_time_line_post(post_id):
    try:
        post = TimelinePost.get_by_id(post_id)
    except TimelinePost.DoesNotExist:
        return jsonify({'error': 'timeline post not found'}), 404

    post.delete_instance()
    return jsonify({'message': 'timeline post deleted', 'id': post_id})


if __name__ == "__main__":
    app.run(debug=True)
