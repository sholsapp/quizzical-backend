from logging import getLogger
import os

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship


log = getLogger(__name__)


db = SQLAlchemy()


class Quiz(db.Model):
  __tablename__ = 'quiz'
  id = Column(Integer, primary_key=True)
  name = Column(String(256))
  question_cnt = Column(Integer)
  questions = relationship('Question', backref='quiz')
  def __repr__(self):
    return '<Quiz %r %r>' % (self.id, self.name)
  def __init__(self, name, question_cnt):
    self.name = name
    self.question_cnt = question_cnt


class Entity(db.Model):
  __tablename__ = 'entity'
  id = Column(Integer, primary_key=True)
  category = Column(String(256))
  name = Column(String(256))
  attributes = relationship('EntityAttr', backref='entity')
  def __repr__(self):
    return '<Entity %r %r>' % (self.id, self.name)
  def __init__(self, name):
    self.name = name


class EntityAttr(db.Model):
  __tablename__ = 'entity_attr'
  id = Column(Integer, primary_key=True)
  entity_id = Column(Integer, ForeignKey('entity.id'))
  attr_name = Column(String(256))
  attr_value = Column(String(256))
  img = Column(LargeBinary)
  def __repr__(self):
    return '<EntityAttr %r %r %r %r>' % (self.id, self.entity_id, self.key, self.value)
  def __init__(self, key, value, img=None):
    self.attr_name = key
    self.attr_value = value
    self.img = img


class QuestionFormat(db.Model):
  __tablename__ = 'question_format'
  id = Column(Integer, primary_key=True)
  format_string = Column(String(256))
  def __repr__(self):
    return '<QuestionFormat %r %r>' % (self.id, self.format_string)
  def __init__(self, format_string):
    self.format_string = format_string


class Question(db.Model):
  __tablename__ = 'question'
  id = Column(Integer, primary_key=True)
  quiz_id = Column(Integer, ForeignKey('quiz.id'))
  entity = Column(String(256))
  attr = Column(String(256))
  format = relationship('QuestionFormat', backref='question', uselist=False)
  def __repr__(self):
    return '<Question %r %r %r>' % (self.id, self.entity, self.attr)
  def tojson(self):
    return {
      'id': self.id,
      'format': self.format.format_string,
      'entity': self.entity,
      'attr_key': self.attr,
    }


def make_conn_str(debug=False):
  if debug:
    log.info('Configuring database in debug mode.')
    return 'sqlite:///quizzical.db'
  else:
    log.info('Configuring database in mysql mode.')
    return os.environ['DATABASE_URL']
