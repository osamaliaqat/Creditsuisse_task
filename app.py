import datetime
import flask
from flask import Flask,  request, jsonify
from models import Base, staging_pg_engine, user, posts
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from utils import get_user

Base.metadata.create_all(staging_pg_engine)

app = Flask(__name__)
app.app_context().push()
app.config["JWT_SECRET_KEY"] = "drake234"
jwt = JWTManager(app)


@app.route("/api/v1/login", methods=['POST'])
def login():
    json = flask.request.json
    email = json['email']
    password = json['password']
    is_user = get_user(email, password)
    if not is_user:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)


@app.route("/create_user", methods=['POST'])
def create_user():
    try:
        json = flask.request.json
        session = Session(bind=staging_pg_engine, expire_on_commit=False)
        email = json['email']
        name = json['name']
        password = json['password']
        users = session.query(user).filter_by(email=email).first()
        if users:
            return 'User Already exists'
        new_user = user(email=email, name=name, password=generate_password_hash(password, method='sha256'))

        session.add(new_user)
        session.commit()
        id = new_user.id
        session.close()

        return f"created user with id {id}"
    except Exception as e:
        print(e)
        return f"Sorry for inconvienience system encountered some problem "


@app.route("/create_post", methods=['POST'])
@jwt_required()
def create_post():
    try:
        session = Session(bind=staging_pg_engine, expire_on_commit=False)
        post_description = request.form.get('description')
        created_at = datetime.datetime.now()
        email = get_jwt_identity()
        user_id = session.query(user).filter_by(email=email).first()

        new_post = posts(user_id=user_id.id, post_description=post_description, created_at= created_at)
        session.add(new_post)
        session.commit()
        id = new_post.id
        session.close()

        return f"created post with id {id}"
    except Exception as e:
        print(e)
        return f"Sorry for inconvienience system encountered some problem "


@app.route('/all_posts', methods=['GET'])
@jwt_required()
def allposts():
    try:
        session = Session(bind=staging_pg_engine, expire_on_commit=False)
        email = get_jwt_identity()
        user_id = session.query(user).filter_by(email=email).first()
        all_posts = session.query(posts).filter_by(user_id=user_id.id).all()

        description = []
        posted_on = []
        for post in all_posts:
            postdescription = post.post_description
            postedon = post.created_at
            description.append(postdescription)
            posted_on.append(postedon)
        return jsonify({"Description": description, "Posted_on": posted_on})
    except Exception as e:
        print(e)
        return f"Sorry for inconvienience system encountered some problem "


@app.route('/update_post/', methods=['PUT'])
@jwt_required()
def update_post():
    try:
        json = flask.request.json
        id = json['id']
        session = Session(bind=staging_pg_engine, expire_on_commit=False)
        data = request.get_json()
        get_post = session.query(posts).get(id)
        if data.get('post_description'):
            get_post.post_description = data['post_description']
        session.add(get_post)
        session.commit()
        session.close()
        return f"post updated successfully"
    except Exception as e:
        print(e)
        return f"Sorry for inconvienience system encountered some problem "


if __name__ == '__main__':
    app.run()
