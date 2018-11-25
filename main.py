from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:1234@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(400))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/', methods=['POST','GET'])
def index():

    posts = Blog.query.all()
    return render_template("home.html", title="Home", blogs=posts)

@app.route('/new_entry', methods = ['POST','GET'])
def new_entry():
    if request.method == 'POST':
        post_name = request.form.get('blog_title')
        post_body = request.form.get('blog_body')
        new_post = Blog(post_name, post_body)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')
    
    return render_template("add_post.html", title="New Post")

@app.route('/post', methods=['POST','GET'])   
def post_page():
    post_id = request.args.get("id")
    post = Blog.query.get(post_id)
    title = post.title
    return render_template("post_page.html", title=title, blog=post)

if __name__ == '__main__':
    app.run()