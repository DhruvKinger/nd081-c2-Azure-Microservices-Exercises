import os

import azure.functions as func
import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


def _get_collection():
    url = os.environ["MyDbConnection"]
    client = pymongo.MongoClient(url)
    database = client["lab2db"]
    return database["notes"]


@app.route(route="getNotes", methods=["GET"])
def get_notes(req: func.HttpRequest) -> func.HttpResponse:
    try:
        result = _get_collection().find({})
        return func.HttpResponse(dumps(result), mimetype="application/json", charset="utf-8")
    except Exception:
        return func.HttpResponse("could not connect to mongodb", status_code=400)


@app.route(route="getNote", methods=["GET"])
def get_note(req: func.HttpRequest) -> func.HttpResponse:
    note_id = req.params.get("id")
    if not note_id:
        return func.HttpResponse("Please pass an id parameter in the query string.", status_code=400)

    try:
        query = {"_id": ObjectId(note_id)}
    except Exception:
        return func.HttpResponse("Invalid id format.", status_code=400)

    try:
        result = _get_collection().find_one(query)
        return func.HttpResponse(dumps(result), mimetype="application/json", charset="utf-8")
    except Exception:
        return func.HttpResponse("Database connection error.", status_code=500)