from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {
  "apiKey": "AIzaSyBTkRd6sHfMXPBZW0qgW1l6eCmBkqXNSo4",
  "authDomain": "csss-17e98.firebaseapp.com",
  "projectId": "csss-17e98",
  "storageBucket": "csss-17e98.appspot.com",
  "messagingSenderId": "304723448287",
  "appId": "1:304723448287:web:b8e8381ce105f4f15ff46a",
  "measurementId": "G-NWP85NS83X",
  "databaseURL": "https://csss-17e98-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"

    return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       user = {'fullname': request.form['full_name'] ,  'username': request.form['username'], 'bio' : request.form['bio']}

       try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('sign_in'))

       except:
            error = "Authentication failed"
            return render_template("signup.html")
    else:
        return render_template("signup.html")





@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        add_tweet = {'title': request.form['title'] ,  'text': request.form['text'], 'uid' : login_session['user']['localId'] }

        try:
            db.child("Tweets").push(add_tweet)
            return redirect(url_for('add_tweet.html'))

        except:
            error = "Authentication failed"
            return render_template("add_tweet.html")
    else:
        return render_template("add_tweet.html")



@app.route('/all_tweets')
def displaytweets():
    tweets = db.child("Tweets").get().val()
    return render_template("tweets.html", tweets=tweets )




@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))



if __name__ == '__main__':
    app.run(debug=True, port=5002)
