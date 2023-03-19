import json
from flask import Flask, render_template, request
from flask_restful import Api, reqparse, Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from func_api import register_api as register_func_api
from session_api import register_api as register_session_api
from models import Base, ChatMessageModel, ChatSessionModel

app = Flask(__name__)
api = Api(app)

db_engine = create_engine('sqlite:///sqlite.chatdb')
ChatSessionModel.metadata.create_all(db_engine)
ChatMessageModel.metadata.create_all(db_engine)

register_func_api(api)
register_session_api(api, db_engine)

@app.route('/', methods=['GET'])
def chat_index():
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def chat_message():
    return {"hello"}

if __name__ == '__main__':
    app.run(debug=True)