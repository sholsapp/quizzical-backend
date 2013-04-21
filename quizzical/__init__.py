import logging

from flask import Flask, render_template, jsonify
from flask.ext.bootstrap import Bootstrap

from quizzical.model import make_conn_str, db
from quizzical.model import Quiz, Entity, EntityAttr, QuestionFormat, Question


app = Flask(__name__)


Bootstrap(app)


def init_logger(debug=False):
  """Setup logging for this and other modules."""
  logger = logging.getLogger(__name__)
  logger.setLevel(logging.DEBUG)
  ch = logging.StreamHandler()
  ch.setLevel(logging.DEBUG)
  formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
  ch.setFormatter(formatter)
  logger.addHandler(ch)


def init_database(debug=False):
  """Setup the database for the webapp."""
  app.config['SQLALCHEMY_DATABASE_URI'] = make_conn_str(debug=debug)
  db.init_app(app)
  db.create_all(app=app)


def init_webapp(debug=False):
  """Setup the webapp."""
  init_logger(debug=debug)
  init_database(debug=debug)
  return app


@app.route('/')
def index():
  return render_template('index.html')


#
# These are logical views on the database tables
#


@app.route('/api/v1/show_quizzes', methods=['GET'])
def show_quizzes():
  quizzes = []
  for quiz in db.session.query(Quiz):
    quizzes.append({
      'id': quiz.id,
      'name': quiz.name,
      'questions': [q.tojson() for q in quiz.questions],
    })
  return jsonify({'rsp': quizzes})


#
# These are raw views on the database tables
#
@app.route('/api/v1/quizzes', methods=['GET'])
def quizzes():
  return jsonify({})


@app.route('/api/v1/quiz/<quizid>', methods=['GET', 'CREATE', 'PUT', 'DELETE'])
def quiz_rest():
  return jsonify({})


@app.route('/api/v1/questions', methods=['GET'])
def questions():
  return jsonify({})

@app.route('/api/v1/question/<questionid>', methods=['GET', 'CREATE', 'PUT', 'DELETE'])
def question_rest():
  return jsonify({})


@app.route('/api/v1/entities', methods=['GET'])
def entities():
  return jsonify({})


@app.route('/api/v1/entity/<entityid>', methods=['GET', 'CREATE', 'PUT', 'DELETE'])
def entity_rest():
  return jsonify({})
