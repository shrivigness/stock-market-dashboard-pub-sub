from flask import Flask, render_template, request, url_for, redirect, session, Response
import pymongo
import bcrypt
from pykafka import KafkaClient
import json
from datetime import datetime


def get_kafka_client():
    return KafkaClient(hosts='kafka1:19092')
#set app as a Flask instance 
app = Flask(__name__)
#encryption relies on secret keys so they could be run
app.secret_key = "testing"
#connoct to your Mongo DB database
client = pymongo.MongoClient("mongodb://mongodb:27017")

#get the database name
db = client.get_database('total_records')
#get the particular collection that contains the data
records = db.register

#assign URLs to have a particular route 
@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    #if method post in index
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        #if found in database showcase that it's found 
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            #hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            #assing them in a dictionary in key value pairs
            user_input = {'name': user, 'email': email, 'password': hashed}
            #insert it in the record collection
            records.insert_one(user_input)
            
            #find the new created account and its email
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            #if registered redirect to logged in as the registered user
            return render_template('logged_in.html', email=new_email,len = 0)
    return render_template('index.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        #check if email exists in database
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)

@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        subscriptions = db["subscriptions"]
        topics_list = []
        for subs in subscriptions.find({"email":email}):
            topics_list.append(subs["topic"])
        return render_template('logged_in.html', email=email,topics_list = topics_list, len=len(topics_list))
    else:
        return redirect(url_for("login"))

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('index.html')

@app.route('/logged_in/topic/<topicname>')
def get_messages(topicname):
    if "email" in session:
        client = get_kafka_client()
        def events():
            for i in client.topics[topicname].get_simple_consumer():
                now = datetime.now()
                yield 'data:{} update on time {}\n\n'.format(json.loads(i.value.decode()),now.strftime("%Y-%m-%d %H:%M:%S"))
        return Response(events(), mimetype="text/event-stream")
    else:
        return redirect(url_for("login"))

@app.route('/available_subs')
def available_subs():
    if "email" in session:
        email = session["email"]
        topics = db["topics"]
        topics_list = []
        for topic in topics.find(   ):
            topics_list.append(topic["topic"])
        return render_template('subscribe.html', email=email,topics_list = topics_list, len=len(topics_list))
    else:
        return redirect(url_for("login"))

@app.route('/unsubscribe')
def available_unsubs():
    if "email" in session:
        email = session["email"]
        subscriptions = db["subscriptions"]
        topics_list = []
        for subs in subscriptions.find({"email":email}):
            topics_list.append(subs["topic"])
        return render_template('unsubscribe.html', email=email,topics_list = topics_list, len=len(topics_list))
    else:
        return redirect(url_for("login"))

@app.route('/unsubscribe/topic/<topicname>')
def unsubscribe(topicname):
    if "email" in session:
        email = session["email"]
        subscriptions = db["subscriptions"]
        if(subscriptions.find_one({"email":email,"topic":topicname})):
            subscriptions.delete_one({"email":email,"topic":topicname})
        topics_list = []
        for subs in subscriptions.find({"email":email}):
            topics_list.append(subs["topic"])
        return render_template('unsubscribe.html', email=email,topics_list = topics_list, len=len(topics_list))
    else:
        return redirect(url_for("login"))

@app.route('/subscribe/topic/<topicname>')
def subscribe(topicname):
    if "email" in session:
        email = session["email"]
        subscriptions = db["subscriptions"]
        if(not(subscriptions.find_one({"email":email,"topic":topicname}))):
            subscriptions.insert_one({"email":email,"topic":topicname})
        topics_list = []
        for subs in subscriptions.find({"email":email}):
            topics_list.append(subs["topic"])
        return redirect(url_for("available_subs"))
    else:
        return redirect(url_for("login"))

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=False)
