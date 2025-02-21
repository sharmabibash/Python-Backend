from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)


with app.app_context():
    db.create_all()  


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('name')
    email = request.form.get('email')

    if not name or not email:
        flash("Both fields are required!", "error")
        return redirect(url_for('index'))

 
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("Email already exists! Try a different one.", "error")
    else:
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash("User added successfully!", "success")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
