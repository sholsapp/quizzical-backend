from logging import getLogger
import os

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship


log = getLogger(__name__)


db = SQLAlchemy()


tag_association_table = Table('tag_associations', db.metadata,
  Column('entity_id', Integer, ForeignKey('entity.id')),
  Column('tag_id', Integer, ForeignKey('tags.id'))
)


class Quiz(db.Model):
  __tablename__ = 'quiz'
  id = Column(Integer, primary_key=True)
  name = Column(String(256))
  questions = relationship('Question', backref='quiz')
  def __repr__(self):
    return '<Quiz %r %r>' % (self.id, self.name)
  def __init__(self, name):
    self.name = name
  def tojson(self):
    return {
      'id': self.id,
      'name': self.name,
      'questions': [q.tojson() for q in self.questions],
    }


class Tag(db.Model):
  __tablename__ = 'tags'
  id = Column(Integer, primary_key=True)
  tag = Column(String, nullable=False, unique=True)
  def __repr__(self):
    return "<Tag('%s', '%s')>" % (self.id, self.tag)
  def tojson(self):
    return self.tag


class Entity(db.Model):
  __tablename__ = 'entity'
  id = Column(Integer, primary_key=True)
  attributes = relationship('EntityAttr', backref='entity')
  tags = relationship('Tag', secondary=tag_association_table)
  def __repr__(self):
    return '<Entity %r>' % (self.id)
  def __init__(self, tags):
    self.tags.extend(tags)
  def tojson(self):
    return {
      'tags': [t.tojson() for t in self.tags],
      'attributes': [a.tojson() for a in self.attributes],
    }


class EntityAttr(db.Model):
  __tablename__ = 'entity_attr'
  id = Column(Integer, primary_key=True)
  entity_id = Column(Integer, ForeignKey('entity.id'))
  attr_name = Column(String(256))
  attr_value = Column(String(256))
  is_img = Column(Boolean(256))
  def __repr__(self):
    return '<EntityAttr %r %r %r %r>' % (self.id, self.entity_id, self.key, self.value)
  def __init__(self, key, value, img=False):
    self.attr_name = key
    self.attr_value = value
    self.is_img = img
  def tojson(self):
    return {
      'attr_name': self.attr_name,
      'attr_value': self.attr_value,
      'img': self.is_img,
    }


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
  tag = Column(String(256))
  attr1 = Column(String(256))
  attr2 = Column(String(256))
  format = relationship('QuestionFormat', backref='question', uselist=False)
  def __repr__(self):
    return '<Question %r %r %r>' % (self.id, self.entity, self.attr)
  def __init__(self, tag, attr1, attr2):
    self.tag = tag
    self.attr1 = attr1
    self.attr2 = attr2
  def tojson(self):
    return {
      'tag': self.tag,
      'attr1': self.attr1,
      'attr2': self.attr2,
    }


def make_conn_str(debug=False):
  if debug:
    log.info('Configuring database in debug mode.')
    return 'sqlite:///quizzical.db'
  else:
    log.info('Configuring database in mysql mode.')
    return os.environ['DATABASE_URL']
