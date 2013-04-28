from random import randint
import logging

from flask import Flask, render_template, jsonify, url_for
from flask.ext.bootstrap import Bootstrap

from quizzical.model import make_conn_str, db
from quizzical.model import Quiz, Entity, EntityAttr, QuestionFormat, Question, Tag


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

@app.route('/api/v1/make_question/<quizid>', methods=['GET'])
def make_question(quizid):
  quiz = db.session.query(Quiz).filter(Quiz.id == quizid).first()
  # Get a random abstract question
  q = quiz.questions[randint(0, len(quiz.questions) - 1)]
  # And get the relevant entities for that abstract question
  entities = db.session.query(Entity).filter(
    Entity.tags.any(tag=q.tag)
  ).all()
  # Randomly select 4 unique entities
  randoms = set()
  while len(randoms) < 4:
    randoms.add(entities[randint(0, len(entities) - 1)])
  randoms = list(randoms)

  def _make_choice(idx, truth):
    return {
      'attr_value': randoms[idx].get_attr(q.attr2).attr_value,
      'correct': truth,
    }

  # Prepare the result object
  question = {
    'question': q.format.format_string % {
      'attr1': randoms[0].get_attr(q.attr2).attr_name.lower(),
      'attr2': randoms[0].get_attr(q.attr1).attr_value,
    },
    'choices': [
      _make_choice(0, True),
      _make_choice(1, False),
      _make_choice(2, False),
      _make_choice(3, False),
    ],
  }
  return jsonify({'rsp': question})

#
# These are raw views on the database tables
#
@app.route('/api/v1/quizzes', methods=['GET'])
def quizzes():
  quizzes = []
  for quiz in db.session.query(Quiz):
    quizzes.append({
      'id': quiz.id,
      'Entity.name': quiz.name,
      'url': 'http://localhost:5000' + url_for('quiz_rest', quizid=quiz.id),
    })
  return jsonify({'rsp': quizzes})


@app.route('/api/v1/quiz/<quizid>', methods=['GET'])
def quiz_rest(quizid):
  quiz = db.session.query(Quiz).filter(Quiz.id == quizid).first()
  return jsonify(quiz.tojson())


@app.route('/api/v1/questions', methods=['GET'])
def questions():
  return jsonify({})


@app.route('/api/v1/question/<questionid>', methods=['GET'])
def question_rest():
  return jsonify({})


@app.route('/api/v1/entities', methods=['GET'])
def entities():
  titties = []
  for e in db.session.query(Entity):
    titties.append({
      'tags': [t.tojson() for t in e.tags],
      'url': 'http://localhost:5000' + url_for('entity_rest', entityid=e.id),
    })
  return jsonify({'rsp': titties})


@app.route('/api/v1/entity/<entityid>', methods=['GET'])
def entity_rest(entityid):
  e = db.session.query(Entity).filter(Entity.id == entityid).first()
  return jsonify(e.tojson())

