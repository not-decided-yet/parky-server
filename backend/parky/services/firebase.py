from parky.constants import FIREBASE_API_KEY, FIREBASE_ALERT_ICON

import requests


class FirebaseService:
    @staticmethod
    def push_message(title: str, body: str, push_token: str):
        """
        Send push message using Firebase Cloud Messaging (FCM).

        :param title: Title of the alert
        :param body: Body string of the alert
        :param push_token: Personal push token
        """
        endpoint = "https://fcm.googleapis.com/fcm/send"
        payload = {
            "notification": {
                "title": title,
                "body": body,
                "icon": FIREBASE_ALERT_ICON,
            },
            "to": push_token,
        }

        response = requests.post(
            endpoint,
            json=payload,
            headers={"Authorization": f"key={FIREBASE_API_KEY}", "Content-Type": "application/json"},
        )
        return response
