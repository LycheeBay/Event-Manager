#https://docs.replit.com/hosting/deploying-http-servers
from flask import Flask, jsonify, request, Response
import auth
import json
import eventcontainer

app = Flask(__name__)
auther = auth.Authenticator()
eventContainer = eventcontainer.EventContainer("")


@app.route('/newuser', methods=['POST'])
def add_user():
  data = request.get_json()
  email = data["email"]
  password = data["password"]
  priv = data["priv"]
  result = auther.has_user(email)
  if result == False:
    auther.add_user(email, password, priv)
    return Response("User added successfully.", status=200)
  else:
    return Response("User already added.", status=404)


@app.route('/auth', methods=['POST'])
def verify_user():
  data = request.get_json()
  email = data["email"]
  password = data["password"]
  result = auther.get_token(email, password)
  if result != "NULL":
    return jsonify(token=result), 200
  else:
    return "User entered wrong credentials.", 404


@app.route('/changepassword', methods=['PUT'])
def update_password():
  data = request.get_json()
  email = data["email"]
  password = data["password"]
  result = auther.has_user(email)
  if result == True:
    auther.change_password(email, password)
    return Response("Password changed.", status=200)
  else:
    return Response("User not found.", status=404)


@app.route('/logout', methods=['PUT'])
def log_out():
  data = request.get_json()
  token = data["token"]
  result = auther.log_out(token)
  if result == True:
    return Response("User logged out.", status=200)
  else:
    return Response("Token not found.", status=404)


@app.route('/events', methods=['POST'])
def get_events():
  data = request.get_json()
  token = data["token"]
  if auther.token_active(token):
    return eventContainer.get_events(), 200
  else:
    return Response("Token not found.", status=404)


@app.route('/events/search/', methods=['POST'])
def search_events():
  data = request.get_json()
  token = data["token"]
  keyword = request.args.get('keyword')
  if auther.token_active(token):
    return jsonify(eventContainer.get_id_by_name(keyword)), 200
  else:
    return Response("Token not found.", status=404)


@app.route('/events', methods=['PUT'])
def add_event():
  data = request.get_json()
  token = data["token"]
  event_info = data["event"]
  print(event_info)
  if auther.get_privilege(token) == 1:
    return jsonify(eventContainer.add_item(json.dumps([event_info]))), 200
  else:
    return Response("Token not found or not authorized.", status=404)


@app.route('/events', methods=['DELETE'])
def delete_event():
  data = request.get_json()
  token = data["token"]
  event_id = data["event-id"]
  if auther.get_privilege(token) == 1:
    if eventContainer.delete_by_id(event_id) == True:
      return "Event removed.", 200
    else:
      return "Event with ID not found.", 201
  else:
    return Response("Token not found or not authorized.", status=404)


app.run(host='0.0.0.0', port=2333)
