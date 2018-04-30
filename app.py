from flask import Flask, jsonify, request, render_template, url_for, redirect
import requests
from datetime import datetime
import json
import os


app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/fillup')
def fillup():
	return render_template('fillup.html')


@app.route('/ask', methods=['GET','POST'])
def question():	
    if request.method == 'POST':
        date = str(datetime.now())
        question_title = request.form['title']
        question_desc = request.form['desc']
        requests.post('http://iitoverflow.herokuapp.com/api/users/1/question', json={"question": question_title,"createdAt": date,  "updatedAt": date,"deletedAt": date,"questiondesc": question_desc, "userId": 1})
        return redirect(url_for('question'))
    return render_template('questions.html')



@app.route('/profile/<int:id>',methods=['GET','POST'])
def profile(id):
    user = str(id)
    url = ('http://iitoverflow.herokuapp.com/api/users/'+user+'?filter[include]=questions&filter[include]=interests')
    print(user)
    response = requests.get(url)
    json_object = response.json()

    curl = ('http://iitoverflow.herokuapp.com/api/users/'+user+'?filter[counts]=followers&filter[counts]=following&filter[include]=followers&filter[include]=following')
    response = requests.get(curl)
    json_object1 = response.json()
    val3 = json_object1['followersCount']
    val4 = json_object1['followingCount']


    return render_template('profile.html', json_object=json_object, json_object1=json_object1, followers=val3, following=val4)


if __name__=='__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host= '0.0.0.0', port=port)