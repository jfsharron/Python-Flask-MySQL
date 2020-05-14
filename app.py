from flask import Flask, url_for
from flask import render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets
from sqlalchemy import or_

""" 
    Code to follow YouTube playlist - https://www.youtube.com/playlist?list=PLUUyxKFz8jHAIc5al0yx_f7qgJvlwU5wB
"""

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)

class colbert_friends_app(db.Model):
    friendId = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

    def __repr__(self):
        return "ID: {0} | first name: {1} | last name: {2}".format(self.id, self.first_name, self.last_name)

class FriendForm(FlaskForm):
    friendId = IntegerField('Friend ID:')
    first_name = StringField('First Name:', validators = [DataRequired()])
    last_name = StringField('Last Name:', validators = [DataRequired()])


@app.route('/')
def index():
    all_friends = colbert_friends_app.query.all()
    return render_template('index.html', friends = all_friends, pageTitle = 'Mike\'s Friends')

@app.route('/search', methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = colbert_friends_app.query.filter(or_(colbert_friends_app.first_name.like(search),
                                                       colbert_friends_app.last_name.like(search))).all()
        return render_template('index.html', friends = results, pageTitle = 'Mike\'s Friends', legend = "Search Results")
    else:
        return redirect('/')


@app.route('/add_friend', methods = ['GET', 'POST'])
def add_friend():
    form = FriendForm()
    if form.validate_on_submit():
        friend = colbert_friends_app(first_name = form.first_name.data, last_name = form.last_name.data)
        db.session.add(friend)
        db.session.commit()
        return redirect('/')

    return render_template('add_friend.html', form = form, pageTitle = 'Add a New Friend',
                            legend = "Add a New Friend")

@app.route('/delete_friend/<int:friend_id>', methods = ['GET', 'POST'])
def delete_friend(friend_id):
    if request.method == 'POST':
        friend = colbert_friends_app.query.get_or_404(friend_id)
        db.session.delete(friend)
        db.session.commit()
        return redirect("/")
    else:
        return redirect("/")

@app.route('/friend/<int:friend_id>', methods = ['GET', 'POST'])
def get_friend(friend_id):
    friend = colbert_friends_app.query.get_or_404(friend_id)
    return render_template('friend.html', form = friend, pageTitle = 'Friend Details', legend = "Friend Details")        

@app.route('/friend/<int:friend_id>/update', methods = ['GET', 'POST'])
def update_friend(friend_id):
    friend = colbert_friends_app.query.get_or_404(friend_id)
    form = FriendForm()

    if form.validate_on_submit():
        friend.first_name = form.first_name.data
        friend.last_name = form.last_name.data
        db.session.commit()
        return redirect(url_for('get_friend', friend_id = friend.friendId))
    form.friendId.data = friend.friendId
    form.first_name.data = friend.first_name
    form.last_name.data = friend.last_name
    return render_template('update_friend.html', form = form, pageTitle = 'Update Friend', legend = "Update a Friend")


if __name__ == '__main__':
    app.run(debug = True)


