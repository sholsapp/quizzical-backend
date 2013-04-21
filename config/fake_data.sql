# Inserts a bunch of fake data into the database for testing
#
# Start by destroying the existing data (if any) and then repopulate

DELETE FROM entity_attr WHERE id > 0;
DELETE FROM entity WHERE id > 0;
DELETE FROM question_format WHERE id > 0;
DELETE FROM question WHERE id > 0;
DELETE FROM quiz WHERE id > 0;

INSERT INTO entity (id, category, name) VALUES
  (1, 'Country', 'USA'),
  (2, 'Country', 'UK'),
  (3, 'Country', 'Canada'),
  (4, 'Country', 'Mexico'),
  (5, 'Fruit', 'Banana'),
  (6, 'Fruit', 'Apple'),
  (7, 'Fruit', 'Orange');

INSERT INTO entity_attr (id, entity_id, attr_name, attr_value) VALUES
  (1, 1, 'name', 'USA'),
  (2, 1, 'population', '1'),
  (3, 2, 'name', 'United Kingdom'),
  (4, 2, 'population', '2'),
  (5, 3, 'name', 'Canada'),
  (6, 3, 'population', '3'),
  (7, 4, 'name', 'Mexico'),
  (8, 4, 'population', '4'),
  (9, 5, 'color', 'Yellow'),
  (10, 6, 'color', 'Red'),
  (11, 7, 'color', 'Orange');

INSERT INTO quiz (id, name) VALUES
  (1, 'Countries'),
  (2, 'Fruits');

INSERT INTO question_format (id, format_string) VALUES
  (1, 'What is the %(attr_name)s of %(entity_name)s?');

INSERT INTO question (id, quiz_id, entity, attr) VALUES
  (1, 1, 'Country', 'population'),
  (2, 1, 'Country', 'name'),
  (3, 2, 'Fruit', 'color');