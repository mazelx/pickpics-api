from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase('database.sqlite')


class Picture(Model):
    id = CharField(unique=True, primary_key=True)
    url = CharField()
    # 1 for picked, -1 for rejected or 0 if unprocessed
    pick_state = SmallIntegerField()

    class Meta:
        database = db


class PickHistory(Model):
    id = CharField(unique=True, primary_key=True)
    picture_id = ForeignKeyField(Picture, backref="picks")

    class Meta:
        database = db


def create_tables():
    with db:
        db.create_tables([Picture, PickHistory])