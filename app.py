from flask import Flask, request, session, \
    abort, jsonify, make_response, Response, json

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

import os
app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)

from models import *

def load_user(user_id):
  user = db.session.query(User).filter(User.userid == user_id).first()
  return user

def load_group(group_id):
  group = db.session.query(Group).filter(Group.name == group_id).first()
  return group

def table_columns(model):
  keys = model.__table__.columns._data.keys()
  keys.remove('id')
  return keys

def is_valid_model_dict(params, model):
  for column in table_columns(model):
    if column in params and type(params[column]) != unicode:
      abort(400)

def is_valid_model_request(request, model):
  if not request.json:
    abort(400)
  for column in table_columns(model):
    if column in request.json and type(request.json[column]) != unicode:
      abort(400)

def save_db_session():
  try:
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    db.session.flush()
    abort(422)
  finally:
    db.session.close()


@app.route("/")
def index():
    return "Welcome to my python assessment."

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(409)
def not_found(error):
    return make_response(jsonify({'error': 'Resource Conflict'}), 409)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Request.'}), 400)

# User Actions

@app.route('/users', methods=['GET'])
def get_users():
    users = db.session.query(User).all()
    if not users:
      abort(404)
    user_array = []
    for user in users:
      groups = [group.name for group in user.groups]
      user_array.append(dict(first_name=user.first_name, last_name=user.last_name, userid=user.userid, groups=groups))
    return jsonify(users=user_array)

@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = load_user(user_id)
    if not user:
      abort(404)
    groups = [group.name for group in user.groups]
    return jsonify(dict(first_name=user.first_name, last_name=user.last_name, userid=user.userid, groups=groups))

@app.route('/users/<string:user_id>', methods=['POST'])
def receive_user(user_id):
    user = load_user(user_id)
    if user:
      abort(409)
    is_valid_model_request(request, User)
    user = User(**request.json)
    db.session.add(user)
    save_db_session()
    user = db.session.merge(user)
    return make_response(jsonify(dict(first_name=user.first_name, last_name=user.last_name, userid=user.userid)), 201)

@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    user = db.session.query(User).filter(User.userid == user_id).first()
    if not user:
      abort(404)
    is_valid_model_request(request, User)
    db.session.query(User).filter_by(userid=user_id).update(request.get_json())
    save_db_session()
    user = db.session.merge(user)
    return make_response(jsonify(dict(first_name=user.first_name, last_name=user.last_name, userid=user.userid)), 202)

@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = load_user(user_id)
    if not user:
      abort(404)
    db.session.delete(user)
    save_db_session()
    return make_response(jsonify({'message': 'Successfully removed user.'}), 200)


# Group Actions

@app.route('/groups', methods=['GET'])
def get_groups():
    groups = db.session.query(Group).all()
    if not groups:
      abort(404)
    group_array = []
    for group in groups:
      users = [user.userid for user in group.users]
      group_array.append(dict(name=group.name, users=users))
    return jsonify(groups=group_array)

@app.route('/groups/<string:group_id>', methods=['GET'])
def get_group(group_id):
    group = load_group(group_id)
    if not group:
      abort(404)
    users = [user.userid for user in group.users]
    return make_response(jsonify(dict(name=group.name, users=users)), 200)

@app.route('/groups/<string:group_id>', methods=['POST'])
def receive_group(group_id):
    group = load_group(group_id)
    if group:
      abort(409)
    is_valid_model_request(request, Group)
    group = Group(**request.json)
    db.session.add(group)
    save_db_session()
    group = db.session.merge(group)
    return make_response(jsonify(dict(name=group.name)), 201)

@app.route('/groups/<string:group_id>', methods=['PUT'])
def update_group(group_id):
    group = db.session.query(Group).filter(Group.name == group_id).first()
    if not group:
      abort(404)

    group_updates = dict(request.get_json())

    group_users = None
    if 'users' in group_updates:
      group_users = group_updates['users']
      group_updates.pop("users", None)

    is_valid_model_dict(group_updates, Group)

    if group_users:
      for user in group_users:
        user = load_user(user)
        if user:
          group.users.append(user)

    db.session.query(Group).filter_by(name=group_id).update(group_updates)
    save_db_session()
    group = db.session.merge(group)
    return make_response(jsonify(dict(name=group.name)), 202)

@app.route('/groups/<string:group_id>', methods=['DELETE'])
def delete_group(group_id):
    group = load_group(group_id)
    if not group:
      abort(404)
    db.session.delete(group)
    save_db_session()
    return make_response(jsonify({'message': 'Successfully removed group.'}), 200)


if __name__ == "__main__":
    app.run(debug=True)
