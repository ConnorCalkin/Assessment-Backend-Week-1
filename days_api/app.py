"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime, date

from flask import Flask, Response, request, jsonify

from date_functions import (convert_to_datetime, get_day_of_week_on,
                            get_days_between, get_current_age)

app_history = []

app = Flask(__name__)


def add_to_history(current_request):
    """Adds a route to the app history."""
    app_history.append({
        "method": current_request.method,
        "at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "route": current_request.endpoint
    })


def clear_history():
    """Clears the app history."""
    app_history.clear()


@app.get("/")
def index():
    """Returns an API welcome messsage."""
    return jsonify({"message": "Welcome to the Days API."})


@app.route("/between", methods=["POST"])
def between():
    add_to_history(request)
    json = request.json

    if "first" not in json or "last" not in json:
        return {
            "error": "Missing required data."
        }, 400

    try:
        first = convert_to_datetime(json["first"])
        last = convert_to_datetime(json["last"])
    except ValueError:
        return {
            "error": "Unable to convert value to datetime."
        }, 400

    return {
        "days": get_days_between(first, last)
    }, 200


@app.route("/weekday", methods=["POST"])
def weekday():
    add_to_history(request)
    json = request.json

    if "date" not in json:
        return {
            "error": "Missing required data."
        }, 400

    try:
        date = convert_to_datetime(json["date"])
    except:
        return {
            "error": "Unable to convert value to datetime."
        }, 400

    return {
        "weekday": get_day_of_week_on(date)
    }


@app.route("/history", methods=["GET", "DELETE"])
def history():
    add_to_history(request)
    if request.method == "GET":
        try:
            number = request.args.get('number')
            if number is None:
                number = 5
            number = int(number)
            if number > 20 or number < 1:
                raise ValueError("No numbers between 1 and 20 allowed")
        except ValueError:
            return {
                "error": "Number must be an integer between 1 and 20."
            }, 400

        return app_history[::-1][:number], 200
    elif request.method == "DELETE":
        clear_history()
        return {
            "status": "History cleared"
        }, 200


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(port=8080, debug=True)
