import json
from uuid import uuid4
from flask import Flask, render_template, request
from flask_restful import Api, reqparse, Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from func_api import register_api
from models import Base, ChatMessageModel, ChatMessageSchema, ChatSessionModel, ChatSessionSchema



def register_api(api, db_engine):
    Base.metadata.bind = db_engine

    session_factory = sessionmaker(bind=db_engine)

    class ChatSession(Resource):
        def get(self, session_id=None):
            # List all sessions or get a specific session by ID
            with session_factory() as db_session:
                if session_id:
                    session = db_session.query(ChatSessionModel).filter_by(id=session_id).first()
                    if not session:
                        return {'message': 'Session not found'}, 404
                    chat_session_schema = ChatSessionSchema()
                    return chat_session_schema.dump(session), 200
                else:
                    sessions = db_session.query(ChatSessionModel).filter_by(is_archived=False).all()
                    chat_session_schema = ChatSessionSchema(many=True)
                    return chat_session_schema.dump([session.__dict__ for session in sessions]), 200

        def post(self):
            # Create a new session
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, required=True)
            parser.add_argument('is_archived', type=bool, required=False, default=False)
            args = parser.parse_args()

            with session_factory() as db_session:
                session = ChatSessionModel(id=uuid4().hex, name=args['name'], is_archived=args['is_archived'])
                db_session.add(session)
                db_session.commit()

                chat_session_schema = ChatSessionSchema()
                return chat_session_schema.dump(session), 201

        def put(self, session_id):
            # Update an existing session
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, required=True)
            parser.add_argument('is_archived', type=bool, required=False)
            args = parser.parse_args()

            with session_factory() as db_session:
                session = db_session.query(ChatSessionModel).filter_by(id=session_id).first()
                if not session:
                    return {'message': 'Session not found'}, 404

                if args['is_archived'] is not None:
                    session.name = args['name']
                    session.is_archived = args['is_archived']

                db_session.commit()

                chat_session_schema = ChatSessionSchema()
                return chat_session_schema.dump(session), 200

        def delete(self, session_id):
            # Delete an existing session
            with session_factory() as db_session:
                session = db_session.query(ChatSessionModel).filter_by(id=session_id).first()
                if not session:
                    return {'message': 'Session not found'}, 404

                db_session.delete(session)
                db_session.commit()

                return {'message': 'Session deleted successfully'}, 200

    class ChatMessage(Resource):
        def get(self, session_id):
            with session_factory() as db_session:
                # List messages for a specific session
                session = db_session.query(ChatSessionModel).filter_by(id=session_id, is_archived=False).first()
                if not session:
                    return {'message': 'Session not found'}, 404

                messages = db_session.query(ChatMessageModel).filter_by(chat_session_id=session_id).all()
                chat_messages_schema = ChatMessageSchema(many=True)
                return chat_messages_schema.dump([message.__dict__ for message in messages]), 200

    api.add_resource(ChatSession, '/v1/sessions', '/vi/sessions/<string:session_id>')
    api.add_resource(ChatMessage, '/v1/sessions/<string:session_id>/messages')
