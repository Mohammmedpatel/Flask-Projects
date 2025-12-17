from flask import jsonify, request,g
from flask_restful import Resource
from app.auth.decorators import token_required
from app.md.models import Notes
from app.md.serde import NotesSchema
from app import db


class NotesListView(Resource):

    @token_required
    def get(self):
        notes= Notes.query.filter_by(user_id=g.user_id).all()
        print(notes)
        return NotesSchema(many=True).dump(notes)
    
    @token_required
    def post(self):

        note=request.get_json()

        new_notes=Notes(data=note["data"], user_id=g.user_id)

        db.session.add(new_notes)
        db.session.commit()

        return NotesSchema().dump(new_notes)
    

class NotesView(Resource):

    @token_required
    def get(self,note_id):
        note= Notes.query.filter_by(user_id=g.user_id, id=note_id).first()
        return NotesSchema().dump(note)
    
 
    @token_required
    def put(self, note_id):
        existing_note= Notes.query.filter_by(user_id=g.user_id, id=note_id).first()

        note=request.get_json()

        existing_note.data=note["data"]

        db.session.commit()

        return NotesSchema().dump(existing_note)
    

    @token_required
    def delete(self, note_id):
        existing_note= Notes.query.filter_by(user_id=g.user_id, id=note_id).first()

        db.session.delete(existing_note)
        db.session.commit()

        return jsonify({"message":"Notes deleted"})