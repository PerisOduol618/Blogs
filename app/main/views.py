from flask import render_template,request,redirect,url_for,abort,jsonify
from . import main
from .forms import UpdateProfile, BlogForm, CommentForm
from .. import db, photos
from flask_login import login_required, current_user
from ..models import User, Blog,Comment
from ..request import get_blogQuotes

# Views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    blogQuote = get_blogQuotes()
    title = 'Home -welcome to My Blogs'
    
    return render_template('index.html',title = title, blogQuote=blogQuote)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form = form)



@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))



@main.route('/blog/new', methods=['GET', 'POST'])
@login_required
def blogs():
    """
    View Blog function that returns the BLog page and data
    """
    blog_form = BlogForm()
    if blog_form.validate_on_submit():
        title_blog= blog_form.title_blog.data
        description = blog_form.description.data
        new_blog = Blog(title_blog=title_blog, description=description, user=current_user)
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('main.theblog'))
    title = 'My Blog'
    return render_template('blogs.html', title=title, blog_form=blog_form)

@main.route('/blog/allblogs', methods=['GET', 'POST'])
@login_required
def theblog():
    blogs = Blog.query.all()
    return render_template('myblogs.html', blogs=blogs)


@main.route('/view/<int:id>', methods=['GET', 'POST'])
@login_required
def view(id):
    blog = Blog.query.get_or_404(id)
    blog_comments = Comment.query.filter_by(blog_id=id).all()
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        new_comment = Comment(blog_id=id, comment=comment_form.comment.data, user=current_user)
        new_comment.save_comment()
    return render_template('view.html', blog=blog, blog_comments=blog_comments, comment_form=comment_form)

@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    blog = Blog.query.get_or_404(id)
    if blog.user != current_user:
        abort(403)
    db.session.delete(blog)
    db.session.commit()
 
    return redirect(url_for('main.theblog'))

@main.route('/Update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_blog(id):
    blog = Blog.query.get_or_404(id)
    if blog.user != current_user:
        abort(403)
    form = BlogForm()
    if form.validate_on_submit():
        blog.title_blog = form.title_blog.data
        blog.description = form.description.data
        db.session.commit()

        return redirect(url_for('main.theblog'))
    elif request.method == 'GET':
        form.title_blog.data = blog.title_blog
        form.description.data = blog.description
    return render_template('update_blog.html', form=form)

@main.route('/delete_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    comment =Comment.query.get_or_404(comment_id)
    if (comment.user.id) != current_user.id:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    return jsonify("Success"),200
 
   