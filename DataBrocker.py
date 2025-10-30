import os
import json
import time
import jwt  # pip install pyjwt requests
import requests

''' ******* restful apis ********
    Kivy doesnt support firebase, you need to utilize rest apis to cumminicate to servers
'''
class DataBrocker:
    def __init__(self):
        self.__sa = None
        with open("lrtserver-a98d5c7d720d.json") as f:
            self.__sa = json.load(f)
            
    def get_auth_token(self):
        # Create JWT payload
        now = int(time.time())
        payload = {
            "iss": self.__sa["client_email"],
            "scope": "https://www.googleapis.com/auth/datastore",
            "aud": self.__sa["token_uri"],   # this stays the same
            "iat": now,
            "exp": now + 60 # valid key for a minute
        }

        # Sign the JWT with the service account's private key
        signed_jwt = jwt.encode(payload, self.__sa["private_key"], algorithm="RS256")

        # Exchange the signed JWT for an access token
        res = requests.post(self.__sa["token_uri"], data={
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": signed_jwt
        })

        #print("TOKEN RESPONSE:", res.json())
        access_token = res.json()["access_token"]

        return access_token

            
    def get_document(self, document_id):
        
        # Firestore REST API URL
        url = f"https://firestore.googleapis.com/v1/projects/{self.__sa['project_id']}/databases/(default)/documents/date_gps_data/{document_id}"

        # Add Bearer token header
        access_token = self.get_auth_token()
        headers = {"Authorization": f"Bearer {access_token}"}

        # Perform GET request
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            doc = response.json()
            print(json.dumps(doc, indent=2))
            return json.dumps(doc)
        else:
            print(f"Error {response.status_code}: {response.text}")