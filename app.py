from flask import Flask, jsonify
import pymongo
import json


app = Flask(__name__)

client = pymongo.MongoClient()
db = client.grouch
courses = db.courses

@app.route('/')
def index():
	return 'test'

@app.route('/spring2016/')
def year():
	schools = set()
	for course in courses.find():
		schools.add(course.get('school'))

	return jsonify({'schools': list(schools)})

@app.route('/spring2016/<school>/')
def for_school(school):
	classes = list()
	for course in courses.find({'school':school}):
		classes.append(course.get('number'))

	return jsonify({'numbers': classes})

@app.route('/spring2016/<school>/<number>')
def single_course(school, number):
	course = courses.find_one({'school':school, 'number':number})
	del course['_id']
	return jsonify(course)



if __name__ == '__main__':


	app.run()
