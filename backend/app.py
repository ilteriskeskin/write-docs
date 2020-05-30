from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'linuxdegilgnulinux'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ilteriskeskin/Belgeler/write-docs/backend/main.db'

CORS(app)

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(80))


class Docs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    user_id = db.Column(db.Integer)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(
                public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid.'}), 401

        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/')
@token_required
def home(current_user):
    return jsonify({'status': True})


@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    users = User.query.all()
    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['password'] = user.password
        output.append(user_data)

    return jsonify({'users': output})


@app.route('/user/<public_id>', methods=['GET'])
def get_one_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['username'] = user.username
    user_data['password'] = user.password

    return jsonify({'user': user_data})


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()),
                    username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})
    


@app.route('/user<public_id>', methods=['PUT'])
def promote_user(public_id):
    return ''


@app.route('/user/<public_id>', methods=['DELETE'])
def delete_user(public_id):
    return ''


@app.route('/docs', methods=['POST'])
@token_required
def create_content(current_user):
    data = request.get_json()

    new_docs = Docs(text=data['text'], user_id=current_user.id)
    db.session.add(new_docs)
    db.session.commit()

    return jsonify({'message': 'New docs created!'})


@app.route('/docs', methods=['GET'])
@token_required
def get_all_docs(current_user):
    docs = Docs.query.all()
    output = []

    for doc in docs:
        doc_data = {}
        doc_data['text'] = doc.text
        doc_data['id'] = doc.id
        output.append(doc_data)

    return jsonify({'docs': output})

@app.route('/docs/<doc_id>', methods=['DELETE'])
@token_required
def remove_doc(current_user, doc_id):
    doc = Docs.query.filter_by(id=doc_id, user_id=current_user.id).first()
    
    if not doc:
        return jsonify({'message': 'No doc found!'})
    
    db.session.delete(doc)
    db.session.commit()
    return jsonify({'message': 'Doc item deleted!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data['username'] or not data['password']:
        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    user = User.query.filter_by(username=data['username']).first()

    if not user:
        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    if check_password_hash(user.password, data['password']):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=5)}, app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
