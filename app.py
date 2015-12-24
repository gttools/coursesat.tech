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

    return jsonify({'schools': schools})

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
    
    return jsonify({'numbers': classes})

@app.route('/spring2016/<school>/<number>')
def single_course(school, number):
    course = courses.find_one({'school':school, 'number':number}, {'_id': 0})

    return jsonify(course)



if __name__ == '__main__':

    app.run()
