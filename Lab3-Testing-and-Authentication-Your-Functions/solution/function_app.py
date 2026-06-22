import json
import os

import azure.functions as func
import pymongo


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


def _get_collection():
    url = os.environ["MyDbConnection"]
    client = pymongo.MongoClient(url)
    database = client["mytestdb"]
    return database["notes"]


@app.route(route="createNote", methods=["POST"])
def create_note(req: func.HttpRequest) -> func.HttpResponse:
    try:
        request = req.get_json()
    except ValueError:
        request = None

    if not request:
        return func.HttpResponse(
            "Please pass the correct JSON format in the body of the request object",
            status_code=400,
        )

    try:
        _get_collection().insert_one(request)
        return func.HttpResponse(json.dumps(request), mimetype="application/json", charset="utf-8")
    except Exception:
        return func.HttpResponse("Database connection error.", status_code=500)