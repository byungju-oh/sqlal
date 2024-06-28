from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Post

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

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
    @login_required
    def new_post():
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            new_post = Post(title=title, content=content)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('new_post.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('login'))
        return render_template('signup.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            flash('Invalid username or password', 'danger')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    return app
