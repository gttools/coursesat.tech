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
    schools = courses.distinct('school')

    response = jsonify({'schools': schools})
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

@app.route('/spring2016/<school>/')
def for_school(school):
    aggregationPipeline = [
        {
            '$match': {
                'school': school
            },
        },
        {
            '$group': {
                '_id': None,
                'classes': {
                    '$push': '$number'
                }
            }
        }
    ]
    result = list(courses.aggregate(aggregationPipeline))
    classes = result[0].get('classes') if len(result) > 0 else None
    
    response = jsonify({'numbers': classes})
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

@app.route('/spring2016/<school>/<number>')
def single_course(school, number):
    course = courses.find_one({'school':school, 'number':number}, {'_id': 0})

    response = jsonify(course)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response



if __name__ == '__main__':

    app.run()
