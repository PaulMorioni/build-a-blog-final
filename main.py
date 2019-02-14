from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:1234@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGc7Fgh45'


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

    post_name = ''
    post_body = ''

    if request.method == 'POST':
        post_name = request.form.get('blog_title')
        post_body = request.form.get('blog_body')

        if post_name:

            if post_body:
                new_post = Blog(post_name, post_body)
                db.session.add(new_post)
                db.session.commit()
                post_id = new_post.id
                post_id_str=str(post_id)
                url = '/post?id=' + post_id_str
                return redirect(url)
            else:
                flash('Body Required')
        else:
            if post_body == "":
                flash('Body Required')
            flash('Title Required')
    
    return render_template("add_post.html", title="New Post", post_name = post_name , post_body = post_body)

@app.route('/post', methods=['POST','GET'])   
def post_page():
    post_id = request.args.get("id")
    post = Blog.query.get(post_id)
    title = post.title
    return render_template("post_page.html", title=title, blog=post)

if __name__ == '__main__':
    app.run()