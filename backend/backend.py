from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
import urllib.parse


encoded_password = urllib.parse.quote_plus('Nurye@68793')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:{encoded_password}@localhost/traffic_light'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)


class Squires(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    junction1 = db.Column(db.String(100))
    junction2 = db.Column(db.String(100))
    junction3 = db.Column(db.String(100))
    junction4 = db.Column(db.String(100))
    google_map = db.Column(db.String(200))
    mtm = db.Column(db.String(100))
    atm = db.Column(db.String(100))
    etm = db.Column(db.String(100))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/dashboard')
@login_required
def dashboard():
    comments = Comment.query.all()
    squires = Squires.query.all()
    return render_template('dashboard.html', comments=comments, squires=squires)


@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        description = request.form['description']
        comment = Comment(name=name, phone=phone, description=description)
        db.session.add(comment)
        db.session.commit()
        return jsonify({'message': 'Comment submitted successfully!'})


@app.route('/add_squire', methods=['GET', 'POST'])
@login_required
def add_squire():
    if request.method == 'POST':
        name = request.form['name']
        junction1 = request.form.get('junction1')
        junction2 = request.form.get('junction2')
        junction3 = request.form.get('junction3')
        junction4 = request.form.get('junction4')
        google_map = request.form.get('google_map')
        mtm = request.form.get('mtm')
        atm = request.form.get('atm')
        etm = request.form.get('etm')
        
        squire = Squires(name=name, junction1=junction1, junction2=junction2, junction3=junction3, 
                         junction4=junction4, google_map=google_map, mtm=mtm, atm=atm, etm=etm)
        
        db.session.add(squire)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_squire.html')



@app.route('/update_squire/<int:id>', methods=['GET', 'POST'])
@login_required
def update_squire(id):
    squire = Squires.query.get_or_404(id)
    if request.method == 'POST':
        squire.name = request.form['name']
        squire.junction1 = request.form.get('junction1', None)
        squire.junction2 = request.form.get('junction2', None)
        squire.junction3 = request.form.get('junction3', None)
        squire.junction4 = request.form.get('junction4', None)
        squire.google_map = request.form.get('google_map', None)
        
     
        if 'mtm' in request.form:
            squire.mtm = request.form['mtm']
        else:
            squire.mtm = None 
      
        if 'atm' in request.form:
            squire.atm = request.form['atm']
        else:
            squire.atm = None  
    
        if 'etm' in request.form:
            squire.etm = request.form['etm']
        else:
            squire.etm = None  
        
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('update_squire.html', squire=squire)



@app.route('/delete_squire/<int:squire_id>', methods=['POST'])
@login_required
def delete_squire(squire_id):
    squire = Squires.query.get_or_404(squire_id)
    db.session.delete(squire)
    db.session.commit()
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
