from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from flask import Blueprint, jsonify, request
from typing import Dict
from kluster.models.users import Users
from kluster import db, mail
from kluster.helpers import query_one_filtered
from flask_mail import Message
from kluster.helpers import mail_composer
import os

notification = Blueprint("notification", __name__, url_prefix="/api/v1/notification")


# query the user DB for the access token of the user
# let this be like a helper function that returns the access and refresh tokens
# token.json file??
def get_user_credentials(user_id: str) -> Dict | None:
    if isinstance(user_id, str):
        user_data = Users.query.filter_by(id=user_id).first_or_404()
        return {
            "google_access_token": user_data["access_token"],
            "google_refresh_Token": user_data["refresh_Token"],
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": os.environ.get("client_id"),
            "client_secret": os.environ.get("client_secret"),
            "scopes": ["https://www.googleapis.com/auth/calendar"],
        }
    return None


@notification.route("/medications/<user_id>", methods=["POST"])
def create_medication(user_id):
    try:
        calender_api = build('calendar', 'v3', credentials=get_user_credentials(user_id))

        event = {
            'summary': 'Google I/O 2015',
            'location': '800 Howard St., San Francisco, CA 94103',
            'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
                'dateTime': '2015-05-28T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2015-05-28T17:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=2'
            ],
            'attendees': [
                {'email': 'lpage@example.com'},
                {'email': 'sbrin@example.com'},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        place_holder = calender_api.events().insert(
            calendarId="primary",
            sendNotification=True,
            body=event,
            start="",
            end="",
        )
    except Exception as exc:
        print(exc)
        return jsonify(
            {
                "message": "Something went wrong when creating this medication",
                "error": "Internal Server Error"
            }
        ), 500
    

@notification.route("/mailing")
def testing():
    if request.method == 'GET':
        recipient = request.form['recipient']
        patient_name = request.form['patient_name']
        subject = request.form['subject']
        medication_name = request.form['medication_name']
        dosage = request.form['dosage']
        scheduled_time = request.form['scheduled_time']
        mail_composer(subject,
                      patient_name,
                      medication_name,
                      dosage,
                      scheduled_time,
                      [recipient])

    return jsonify(
        {
            "message": 'Email sent!',
            "data": "done",
            }
    ), 200