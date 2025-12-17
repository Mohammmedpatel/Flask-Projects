from flask_restful import Api
from flask import Blueprint

from app.md.controllers.notes import NotesListView, NotesView


md_blueprint=Blueprint("md",__name__,url_prefix="/md")
api=Api(md_blueprint)

api.add_resource(NotesListView,"/note")
api.add_resource(NotesView,"/note/<int:note_id>")