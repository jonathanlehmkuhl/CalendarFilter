import re

import requests
from flask import Flask, Response, abort, request
from ics import Calendar


def download_calendar(url):
    response = requests.get(url)
    if response.status_code == 200:
        calendar = Calendar(response.content.decode("utf-8"))
        return calendar
    else:
        abort(
            400,
            description=f"Failed to download the calendar. Status code: {response.status_code}",
        )


def filter_calendar(calendar, patterns):
    filtered_calendar = Calendar()
    for event in calendar.events:
        if any(re.search(pattern, event.name) for pattern in patterns):
            filtered_calendar.events.add(event)
    return str(filtered_calendar)


app = Flask(__name__)


@app.route("/calendar-filter")
def serve_filtered_calendar():
    calendar_url = request.args.get("url")
    if not calendar_url:
        abort(400, description="Missing 'url' parameter")

    patterns = request.args.get("patterns")
    if not patterns:
        abort(400, description="Missing 'patterns' parameter")

    calendar = download_calendar(calendar_url)
    patterns_list = [patterns.strip() for pattern in patterns.split(",")]
    filtered_calender = filter_calendar(calendar, patterns_list)

    try:
        response = Response(filtered_calender)
        response.headers["Content-Type"] = "text/calendar"
        response.headers["Content-Disposition"] = "attachment; filename=calendar.ics"
        return response
    except Exception as e:
        abort(500, description=f"Failed to download or filter the calendar: {str(e)}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
