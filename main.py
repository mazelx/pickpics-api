from flask import Flask
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from flask_cors import CORS
import models
from models import Picture
from playhouse.shortcuts import model_to_dict


app = Flask(__name__)
api = Api(app)
cors = CORS(app)

models.create_tables()

picture_fields = {"id": fields.String,
               "url": fields.String,
               "pick_state": fields.Integer,
               }

parser = reqparse.RequestParser()
parser.add_argument('url', required=True, help='Url to image')
parser.add_argument('pick_state', type=int, help='-1 for rejected, 1 for picked, 0 if unprocessed')


class PictureDoc(Resource):
    @marshal_with(picture_fields)
    def get(self, id):
        pic = Picture.get_by_id(id)
        return model_to_dict(pic)

    def put(self, id):
        args = parser.parse_args()
        pic, created = Picture.get_or_create(
            id=id,
            defaults={
                'url': args['url'],
                'pick_state': int(args["pick_state"] or "0")}
        )
        return model_to_dict(pic)


class PictureList(Resource):
    @marshal_with(picture_fields)
    def get(self):
        pics = Picture.select().execute()
        return list(pics)


api.add_resource(PictureDoc, '/pickpics/pictures/<string:id>')
api.add_resource(PictureList, '/pickpics/pictures')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
