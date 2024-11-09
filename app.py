from flask import Flask, request, render_template, redirect, session, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from email_validator import validate_email, EmailNotValidError
from datetime import timedelta
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Session security configuration
def secret_key():
    return secrets.token_hex(16)  

app.secret_key = secret_key() 
app.config['SESSION_COOKIE_SECURE'] = False  # Enable only in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent access by JavaScript
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Session timeout

def generate_token_admin():
    return secrets.token_hex(16)  

def generate_token():
    return secrets.token_hex(16)  

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    token = db.Column(db.String(100), nullable=True, default= None)
    survey = db.Column(db.Boolean, default=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    token = db.Column(db.String(100), nullable=True)
    satisfied_count = db.Column(db.Boolean, default=False) 
    dissatisfied_count = db.Column(db.Boolean, default=False)  
    survey_count = db.Column(db.Boolean, default=False)  

with app.app_context():
    db.create_all()
    
    if not Admin.query.filter_by(email='admin@admin').first():
        admin = Admin(email='admin@admin', password=bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
        db.session.add(admin)
        db.session.commit()

# Routes

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    error_msg = session.pop('error', None)  
    return render_template('login.html', error=error_msg)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        try:
            valid = validate_email(email)
            email = valid.email 
        except EmailNotValidError as e:
            session['error'] = f"Email tidak valid!"
            return redirect('/register') 

        if User.query.filter_by(email=email).first():
            session['error'] = "Email sudah terdaftar!"
            return redirect('/register')  

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        session['success'] = "Registrasi berhasil, silahkan login!"
        return redirect('/register')

    # Clear messages
    success_msg = session.pop('success', None)
    error_msg = session.pop('error', None)
    return render_template('register.html', success=success_msg, error=error_msg)


@app.route('/do_login', methods=['POST'])
def do_login():
    email = request.form['email']
    password = request.form['password']

    # Admin check
    admin = Admin.query.filter_by(email=email).first()
    if admin and bcrypt.checkpw(password.encode('utf-8'), admin.password.encode('utf-8')):
        token = generate_token_admin()
        session['admin_token'] = token
        session.permanent = True  

        admin.token = token
        db.session.commit()  
        return redirect('/dashboard_admin')

    # User check
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        token = generate_token()
        session['user_token'] = token
        session.permanent = True  

        user.token = token
        db.session.commit() 

        return redirect('/dashboard_users')

    session['error'] = 'Kredensial anda tidak valid'
    return redirect('/login')


@app.route('/dashboard_admin')
def admin_dashboard():
    if 'admin_token' not in session:
        abort(403)  
    token = session['admin_token']
    return redirect(f'http://localhost:8501/?sessionToken={token}')


@app.route('/dashboard_users')
def user_dashboard():
    if 'user_token' not in session:
        abort(403)  
    token = session['user_token']
    return redirect(f'http://localhost:8502/?sessionToken={token}')


@app.route('/logout')
def logout():
    token = session.pop('user_token', None)
    if token:
        user = User.query.filter_by(token=token).first()
        if user:
            user.token = None  
            db.session.commit()  

    return redirect('/login')



@app.route('/admin_logout')
def admin_logout():
    token = session.pop('admin_token', None)
    if token:
        admin = Admin.query.filter_by(token=token).first()
        if admin:
            admin.token = None  
            db.session.commit()  

    return redirect('/login')


@app.route('/get_users', methods=['GET'])
def get_users():
    # if 'admin_token' not in session:
    #     return jsonify({'message': 'Unauthorized access'}), 403
    
    users = User.query.all()
    users_data = [{'id': user.id, 'name': user.name, 'email': user.email, 'token': user.token} for user in users]
    return jsonify(users_data), 200


# @app.route('/delete_user/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     if 'admin_token' not in session:
#         return jsonify({'message': 'Unauthorized access'}), 403

#     user = User.query.get(user_id)
#     if user:
#         db.session.delete(user)
#         db.session.commit()
#         return jsonify({'message': 'User deleted successfully'}), 200
#     else:
#         return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
