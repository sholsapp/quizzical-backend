from logging import getLogger
import os

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


log = getLogger(__name__)


db = SQLAlchemy()


class Quiz(db.Model):
  __tablename__ = 'quiz'
  id = Column(Integer, primary_key=True)
  name = Column(String(256))
  questions = relationship('Question', backref='quiz')
  def __repr__(self):
    return '<Quiz %r %r>' % (self.id, self.name)
  def __init__(self, name):
    self.name = name


class Entity(db.Model):
  __tablename__ = 'entity'
  id = Column(Integer, primary_key=True)
  question_id = Column(Integer, ForeignKey('question.id'))
  name = Column(String(256))
  desc = Column(String(256))
  attributes = relationship('EntityAttr', backref='entity')
  def __repr__(self):
    return '<Entity %r %r>' % (self.id, self.name)
  def __init__(self, name, desc=None):
    self.name = name
    self.desc = desc


class EntityAttr(db.Model):
  __tablename__ = 'entity_attr'
  id = Column(Integer, primary_key=True)
  entity_id = Column(Integer, ForeignKey('entity.id'))
  question_id = Column(Integer, ForeignKey('question.id'))
  key = Column(String(256))
  value = Column(String(256))
  desc = Column(String(256))
  def __repr__(self):
    return '<EntityAttr %r %r %r %r>' % (self.id, self.entity_id, self.key, self.value)
  def __init__(self, key, value, desc=None):
    self.key = key
    self.value = value
    self.desc = desc


class QuestionFormat(db.Model):
  __tablename__ = 'question_format'
  id = Column(Integer, primary_key=True)
  question_id = Column(Integer, ForeignKey('question.id'))
  format_string = Column(String(256))
  def __repr__(self):
    return '<QuestionFormat %r %r>' % (self.id, self.format_string)
  def __init__(self, format_string):
    self.format_string = format_string


class Question(db.Model):
  __tablename__ = 'question'
  id = Column(Integer, primary_key=True)
  quiz_id = Column(Integer, ForeignKey('quiz.id'))
  format = relationship('QuestionFormat', backref='question', uselist=False)
  entity = relationship('Entity', backref='question', uselist=False)
  attr = relationship('EntityAttr', backref='question', uselist=False)
  def __repr__(self):
    return '<Question %r>' % (self.id)
  def tojson(self):
    return {
      'id': self.id,
      'format': self.format.format_string,
      'entity': self.entity.name,
      'attr_key': self.attr.key,
      'attr_value': self.attr.value,
    }


def make_conn_str(debug=False):
  """Make an in memory database for now."""
  if debug:
    log.info('Configuring database in debug mode.')
    return 'sqlite:///quizzical.db'
  else:
    log.info('Configuring database in mysql mode.')
    return os.environ['DATABASE_URL']
