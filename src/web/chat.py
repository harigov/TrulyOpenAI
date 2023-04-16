import json
from flask import Flask, render_template, request
from flask_restful import Api, reqparse, Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from func_api import register_api as register_func_api
from session_api import register_api as register_session_api
from models import Base, ChatMessageModel, ChatSessionModel

import ai

app = Flask(__name__)
api = Api(app)

db_engine = create_engine('sqlite:///db.sqlite')
ChatSessionModel.metadata.create_all(db_engine)
ChatMessageModel.metadata.create_all(db_engine)

register_func_api(api)
register_session_api(api, db_engine)

@app.route('/', methods=['GET'])
def chat_index():
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def chat_message():
    with Session(db_engine) as db_session:
        message_objs = db_session.query(ChatMessageModel).filter_by(id=request.json['session_id']).all()
        messages = [
            {
                'role': message_obj.role,
                'content': message_obj.content,
            }
            for message_obj in message_objs
        ]
        messages.append({
            'role': 'user',
            'content': request.json['content'],
        })
        response = ai.chat_completion(messages)

        user_message = ChatMessageModel(
            chat_session_id=request.json['session_id'],
            role='user',
            content=request.json['content']
        )
        ai_response = ChatMessageModel(
            chat_session_id=request.json['session_id'],
            role='assistant',
            content=response,
        )
        db_session.add(user_message)
        db_session.add(ai_response)
        db_session.commit()
        return {"message": response}

if __name__ == '__main__':
    app.run(debug=True)