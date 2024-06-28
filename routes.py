from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import db, Post

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return render_template('index.html', posts=posts)

    @app.route('/post/<int:id>')
    def get_post(id):
        post = Post.query.get_or_404(id)
        return render_template('post.html', post=post)

    @app.route('/new_post', methods=['GET', 'POST'])
    def new_post():
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            new_post = Post(title=title, content=content)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('new_post.html')

    return app
