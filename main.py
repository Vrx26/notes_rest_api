import json
from flask import Flask, jsonify, request
from db_model import db, Notes
from sqlalchemy import or_


app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.sqlite3'
db.init_app(app)

with app.app_context():
    db.create_all()

# Функция реализующая добавление заметок. Принимает на вход POST запрос с данными в формате json.
# Пример запроса:
# curl -H "Content-Type: application/json" -X POST --data '{"title":"test","content":"test_content"}' 127.0.0.1:5000/notes
@app.route('/notes', methods=['POST'])
def post_note():
    new_note = Notes(title=request.json['title'], content=request.json['content'])
    db.session.add(new_note)
    db.session.commit()
    return jsonify(new_note.serialize())

# Функция реализующая получение всех заметок и получение заметок всех заметок содержащих в себе переданный запрос.
# Пример запроса для получения всех заметок:
# curl -X GET 127.0.0.1:5000/notes
# Пример запроса для получения заметок по запросу
# curl -X GET 127.0.0.1:5000/notes?query=test
@app.route('/notes', methods=['GET'])
def get_notes():
    query = request.args.get("query")
    if query is None:
        result = [note.serialize() for note in Notes.query.all()]
        return jsonify(result)
    else:
        result = [res.serialize() for res in db.session.query(Notes).filter(or_(Notes.title.contains(query), Notes.content.contains(query)))]
        return jsonify(result)

# Функция реализующая получение заметки по id
# curl -X GET 127.0.0.1:5000/notes/1
@app.route('/notes/<id>', methods=['GET'])
def get_note_by_id(id):
    note = Notes.query.get(id)
    return jsonify(note.serialize())

# Функция реализующая обновление заметки по id
# curl -H "Content-Type: application/json" -X PUT --data '{"title":"new_title","content":"new_content"}' 127.0.0.1:5000/notes/1
@app.route('/notes/<id>', methods=['PUT'])
def update_note_by_id(id):
    try:
        title=request.json['title']
    except:
        title=None
    try:
        content=request.json['content']
    except:
        content=None
    print(request.json["title"])
    note = Notes.query.get(id)
    if title:
        note.title = title
    if content:
        note.content = content
    db.session.commit()
    return jsonify(note.serialize())

# Функция реализующая удаление заметки по id
# curl -X DELETE 127.0.0.1:5000/notes/1
@app.route('/notes/<id>', methods=['DELETE'])
def delete_note_by_id(id):
    note = Notes.query.get(id)
    if note:
        db.session.delete(note)
        db.session.commit()
        resp = jsonify()
        resp.status_code = 200
        return resp
    else:
        resp = jsonify()
        resp.status_code = 404
        return resp


app.run(debug=True)