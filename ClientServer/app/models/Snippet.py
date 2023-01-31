from sqlalchemy import Column, Integer, String, ForeignKey
from ClientServer.app.models.db_config import db


class Snippet(db.Model):
    __tablename__ = 'snippets'
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.id'))
    size = Column(Integer, default=0)
    data_node = Column(String(120), nullable=False)
    index = Column(Integer, nullable=False)


def insert_snippet(file_id, data_node, index, size):
    snippet = Snippet(file_id=file_id, data_node=data_node, index=index, size=size)
    db.session.add(snippet)
    db.session.commit()


def get_file_snippets(file_id):
    return Snippet.query.filter_by(file_id=file_id)


def delete_file_snippets(file_id):
    Snippet.query.filter_by(file_id=file_id).delete()
    db.session.commit()

