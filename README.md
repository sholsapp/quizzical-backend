quizzical-backend
=================

The backend API that serves data that can be used to build a quiz game.

todo
====

Figure out where to get some test data.

For now, can run code like this in a Flask app to generate data:

```python
  quiz = Quiz('quiz1')
  entity1 = Entity('California')
  entity1attr = EntityAttr('capital', 'Sacramento')
  question_format = QuestionFormat('What is the %(attr)s of %(entity)s?')
  question1 = Question()
  question1.format = question_format
  question1.entity = entity1
  question1.attr = entity1attr
  quiz.questions.append(question1)
  db.session.add(quiz)
  db.session.add(question1)
  db.session.commit()
```
