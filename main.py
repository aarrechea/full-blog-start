from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date




""" -----------------------------------------------------------------------------------------------
Creating the Flask object
----------------------------------------------------------------------------------------------- """
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)




""" ----------------------------------------------------------------------------------------------- 
Connect to database
----------------------------------------------------------------------------------------------- """
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




""" ----------------------------------------------------------------------------------------------- 
Configuring database BlogPost table
----------------------------------------------------------------------------------------------- """
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)




""" ----------------------------------------------------------------------------------------------- 
 WTForm including CKEditor fields in a flask form
----------------------------------------------------------------------------------------------- """
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])

    # Notice body's StringField changed to CKEditorField
    body = CKEditorField("Blog Content", validators=[DataRequired()])

    submit = SubmitField("Submit Post")




""" -----------------------------------------------------------------------------------------------
Getting all posts 
----------------------------------------------------------------------------------------------- """
def function_get_all_posts():
    return BlogPost.query.all()




""" -----------------------------------------------------------------------------------------------
 Home 
----------------------------------------------------------------------------------------------- """
@app.route('/')
def get_all_posts():
    posts = function_get_all_posts()
    return render_template("index.html", all_posts=posts)




""" -----------------------------------------------------------------------------------------------
Create new post
----------------------------------------------------------------------------------------------- """
@app.route("/new-post", methods=["GET", "POST"])
def new_post():
    form = CreatePostForm()

    # POST
    if form.validate_on_submit():
        new_blog = BlogPost(
            title = request.form.get("title"),
            subtitle = request.form.get("subtitle"),
            date = date.today().strftime("%B %d, %Y"),
            body = request.form.get("body"),
            author = request.form.get("author"),
            img_url = request.form.get("img_url")
        )
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for("get_all_posts"))

    # GET
    return render_template("make-post.html", form=form, action="New Post")




""" ----------------------------------------------------------------------------------------------- 
Get a particular post
----------------------------------------------------------------------------------------------- """
@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    posts = function_get_all_posts()
    for blog_post in posts:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)




""" ----------------------------------------------------------------------------------------------- 
 Edit post
----------------------------------------------------------------------------------------------- """
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )

    # POST
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", index=post_id))

    # GET
    return render_template("make-post.html", form=edit_form, action="Edit post")




""" ----------------------------------------------------------------------------------------------- 
 Delete post
----------------------------------------------------------------------------------------------- """
@app.route("/delete/<int:post_id>", methods=["GET"])
def delete_post(post_id):
    post = BlogPost.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("get_all_posts"))




@app.route("/about")
def about():
    return render_template("about.html")




@app.route("/contact")
def contact():
    return render_template("contact.html")




""" ----------------------------------------------------------------------------------------------- 
Running the application
----------------------------------------------------------------------------------------------- """
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)




















